from uuid import UUID, uuid4
from datetime import datetime, timezone
from typing import List, Dict, Any, Optional, AsyncIterator
import json
import logging

from app.schemas.chat import (
    ConversationResponse, MessageResponse, AIWorkoutRecommendation,
    StructuredExerciseRef
)
from app.core.safety_rules import SafetyEngine, SafetySeverity
from app.services.profile_service import ProfileService
from app.services.context_builder import ContextBuilder
from app.services.system_prompts import (
    FITGUIDE_SYSTEM_PROMPT,
    WORKOUT_RECOMMENDATION_SYSTEM_PROMPT,
    build_user_context_block
)
from app.services.llm_service import llm_service
from app.core.rate_limiter import chat_rate_limiter
from app.rag.retrieval import rag_service
from app.services.intent_router import intent_router

logger = logging.getLogger(__name__)

# In-memory stores for fast retrieval and test isolation
_CONVERSATIONS_STORE: Dict[UUID, Dict[str, Any]] = {}
_MESSAGES_STORE: Dict[UUID, List[Dict[str, Any]]] = {} # conversation_id -> messages

class ChatService:
    """
    Orchestrates conversation lifecycle, grounded context construction,
    safety validation, streaming SSE generation, and structured outputs.
    """

    @classmethod
    def list_conversations(cls, user_id: UUID) -> List[ConversationResponse]:
        user_threads = [
            conv for conv in _CONVERSATIONS_STORE.values()
            if conv.get("user_id") == user_id
        ]
        # Sort by updated_at descending
        user_threads.sort(key=lambda x: x["updated_at"], reverse=True)

        return [
            ConversationResponse(
                id=str(conv["id"]),
                user_id=str(conv["user_id"]),
                title=conv["title"],
                created_at=conv["created_at"].isoformat(),
                updated_at=conv["updated_at"].isoformat(),
                message_count=len(_MESSAGES_STORE.get(conv["id"], []))
            )
            for conv in user_threads
        ]

    @classmethod
    def create_conversation(cls, user_id: UUID, title: Optional[str] = None) -> ConversationResponse:
        now = datetime.now(timezone.utc)
        conv_id = uuid4()
        initial_title = title.strip() if title and title.strip() else "New Consultation"
        
        record = {
            "id": conv_id,
            "user_id": user_id,
            "title": initial_title,
            "created_at": now,
            "updated_at": now
        }
        _CONVERSATIONS_STORE[conv_id] = record
        _MESSAGES_STORE[conv_id] = []

        return ConversationResponse(
            id=str(conv_id),
            user_id=str(user_id),
            title=record["title"],
            created_at=now.isoformat(),
            updated_at=now.isoformat(),
            message_count=0
        )

    @classmethod
    def get_conversation_messages(cls, user_id: UUID, conversation_id: UUID) -> List[MessageResponse]:
        conv = _CONVERSATIONS_STORE.get(conversation_id)
        if not conv or conv.get("user_id") != user_id:
            raise KeyError("Conversation not found or access denied")

        msgs = _MESSAGES_STORE.get(conversation_id, [])
        return [
            MessageResponse(
                id=str(m["id"]),
                conversation_id=str(conversation_id),
                sender_role=m["sender_role"],
                content=m["content"],
                citations=m.get("citations"),
                recommendation=m.get("recommendation"),
                created_at=m["created_at"].isoformat()
            )
            for m in msgs
        ]

    @classmethod
    def validate_access(cls, user_id: UUID, conversation_id: UUID) -> Dict[str, Any]:
        conv = _CONVERSATIONS_STORE.get(conversation_id)
        if not conv or conv.get("user_id") != user_id:
            raise KeyError("Conversation not found or unauthorized")
        return conv

    @classmethod
    async def process_message_stream(
        cls, user_id: UUID, conversation_id: UUID, user_prompt: str
    ) -> AsyncIterator[str]:
        """
        Processes an incoming user message:
        1. Validates user prompt against SafetyEngine.
        2. If critical red flag -> intercepts and yields safety advisory immediately.
        3. If safe -> assembles athletic context, queries LLM stream, and yields SSE tokens.
        4. Persists conversation and message history.
        """
        conv = cls.validate_access(user_id, conversation_id)
        now = datetime.now(timezone.utc)

        # Persist user message
        user_msg_id = uuid4()
        user_msg = {
            "id": user_msg_id,
            "conversation_id": conversation_id,
            "sender_role": "user",
            "content": user_prompt,
            "created_at": now
        }
        _MESSAGES_STORE.setdefault(conversation_id, []).append(user_msg)

        # Update conversation title if first message
        if conv["title"] == "New Consultation" and len(_MESSAGES_STORE[conversation_id]) <= 2:
            snippet = user_prompt[:40] + ("..." if len(user_prompt) > 40 else "")
            conv["title"] = snippet

        conv["updated_at"] = now

        # 2. Safety Evaluation
        prefs = ProfileService.get_preferences(user_id)
        age_group = prefs.age_group.value if prefs else "adult_18_64"
        safety_eval = SafetyEngine.evaluate_inbound_prompt(user_prompt, age_group)

        if safety_eval.severity == SafetySeverity.CRITICAL_STOP:
            # Yield metadata event
            yield f"event: meta\ndata: {json.dumps({'status': 'safety_stop', 'rule': safety_eval.triggered_rule})}\n\n"
            
            # Format clinical advisory intervention
            advisory_content = (
                f"### SAFETY INTERVENTION: {safety_eval.triggered_rule.upper().replace('_', ' ')}\n\n"
                f"{safety_eval.user_message}\n\n"
                f"**Clinical Directive**: {safety_eval.suggested_action or 'Please stop physical exertion and seek advice from a licensed medical professional.'}\n\n"
                "*FitGuide AI prioritizes athlete safety above all training objectives.*"
            )

            # Stream advisory tokens
            tokens = advisory_content.split(" ")
            for i, token in enumerate(tokens):
                chunk = token + (" " if i < len(tokens) - 1 else "")
                yield f"event: token\ndata: {json.dumps({'token': chunk})}\n\n"

            # Persist assistant response
            asst_msg_id = uuid4()
            asst_msg = {
                "id": asst_msg_id,
                "conversation_id": conversation_id,
                "sender_role": "assistant",
                "content": advisory_content,
                "created_at": datetime.now(timezone.utc)
            }
            _MESSAGES_STORE[conversation_id].append(asst_msg)

            yield f"event: done\ndata: {json.dumps({'message_id': str(asst_msg_id), 'status': 'completed'})}\n\n"
            return

        # 3. Context & RAG Knowledge Retrieval
        user_context_str = ContextBuilder.build_user_context(user_id)
        secured_context = build_user_context_block(user_context_str)

        # Retrieve relevant scientific knowledge chunks
        retrieved_results = await rag_service.retrieve(
            query=user_prompt,
            age_group=age_group,
            top_k=3,
            threshold=0.55
        )

        # Factual query keywords check for weak-retrieval refusal
        factual_keywords = [
            "according to", "guideline", "scientific", "study", "research",
            "evidence", "clinical", "recommendation", "who say", "acsm say",
            "issn say", "cdc say", "nia say", "nsca say", "citation"
        ]
        is_factual_query = any(k in user_prompt.lower() for k in factual_keywords)

        if is_factual_query and rag_service.is_weak_retrieval(retrieved_results, threshold=0.65):
            # Insufficient evidence fallback
            yield f"event: meta\ndata: {json.dumps({'status': 'weak_retrieval'})}\n\n"
            insufficient_msg = rag_service.get_fallback_insufficient_info_message()
            tokens = insufficient_msg.split(" ")
            for i, token in enumerate(tokens):
                chunk = token + (" " if i < len(tokens) - 1 else "")
                yield f"event: token\ndata: {json.dumps({'token': chunk})}\n\n"

            asst_msg_id = uuid4()
            asst_msg = {
                "id": asst_msg_id,
                "conversation_id": conversation_id,
                "sender_role": "assistant",
                "content": insufficient_msg,
                "citations": None,
                "created_at": datetime.now(timezone.utc)
            }
            _MESSAGES_STORE[conversation_id].append(asst_msg)
            yield f"event: done\ndata: {json.dumps({'message_id': str(asst_msg_id), 'status': 'completed'})}\n\n"
            return

        citations = []
        rag_prompt_addition = ""
        if retrieved_results and not rag_service.is_weak_retrieval(retrieved_results, threshold=0.55):
            rag_prompt_addition, citations = rag_service.format_grounded_context(retrieved_results)
            yield f"event: citations\ndata: {json.dumps({'citations': citations})}\n\n"

        augmented_system_prompt = f"{FITGUIDE_SYSTEM_PROMPT}\n\n{secured_context}"
        if rag_prompt_addition:
            augmented_system_prompt += f"\n\n{rag_prompt_addition}"

        # Classify intent for intelligent downstream routing
        intent_info = intent_router.classify_intent(user_prompt)

        # Yield meta event
        yield f"event: meta\ndata: {json.dumps({'status': 'generating', 'safety_cleared': True, 'intent': intent_info['intent'], 'routing_target': intent_info['routing_target'], 'rag_grounded': bool(citations)})}\n\n"

        # 4. Stream Tokens from LLM
        history = [
            {"role": m["sender_role"], "content": m["content"]}
            for m in _MESSAGES_STORE[conversation_id][-6:]
        ]

        full_response_text = ""
        try:
            async for token in llm_service.stream_text(user_prompt, augmented_system_prompt, history):
                full_response_text += token
                yield f"event: token\ndata: {json.dumps({'token': token})}\n\n"
        except Exception as e:
            logger.error(f"Error during stream generation: {e}")
            error_chunk = "\n\n*[A temporary network issue occurred during streaming. Guidance was grounded on active profile.]*"
            full_response_text += error_chunk
            yield f"event: token\ndata: {json.dumps({'token': error_chunk})}\n\n"

        # 5. Persist Assistant Response
        asst_msg_id = uuid4()
        asst_msg = {
            "id": asst_msg_id,
            "conversation_id": conversation_id,
            "sender_role": "assistant",
            "content": full_response_text,
            "citations": citations if citations else None,
            "created_at": datetime.now(timezone.utc)
        }
        _MESSAGES_STORE[conversation_id].append(asst_msg)

        yield f"event: done\ndata: {json.dumps({'message_id': str(asst_msg_id), 'status': 'completed'})}\n\n"

    @classmethod
    async def generate_workout_recommendation(
        cls, user_id: UUID, prompt: str
    ) -> AIWorkoutRecommendation:
        """
        Generates a validated structured workout recommendation.
        Enforces safety rules and validates schema with Pydantic.
        """
        chat_rate_limiter.check_rate_limit(str(user_id))

        prefs = ProfileService.get_preferences(user_id)
        age_group = prefs.age_group.value if prefs else "adult_18_64"
        safety_eval = SafetyEngine.evaluate_inbound_prompt(prompt, age_group)

        if safety_eval.severity == SafetySeverity.CRITICAL_STOP:
            raise ValueError(f"Safety restriction triggered: {safety_eval.user_message}")

        user_context_str = ContextBuilder.build_user_context(user_id)
        recommendation = await llm_service.generate_workout_recommendation(prompt, user_context_str)

        return recommendation
