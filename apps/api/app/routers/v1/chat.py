from typing import List
from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import StreamingResponse

from app.core.rate_limiter import chat_rate_limiter
from app.core.security import get_current_user, CurrentUser
from app.schemas.chat import (
    ConversationCreate, ConversationResponse, MessageCreate,
    MessageResponse, AIWorkoutRecommendation
)
from app.services.chat_service import ChatService

router = APIRouter(prefix="/chat", tags=["AI Assistant & Chat"])

@router.get("/conversations", response_model=List[ConversationResponse])
async def list_conversations(
    current_user: CurrentUser = Depends(get_current_user)
):
    """
    Retrieves all conversation threads belonging to the authenticated user.
    """
    return ChatService.list_conversations(user_id=current_user.user_id)

@router.post("/conversations", response_model=ConversationResponse, status_code=status.HTTP_201_CREATED)
async def create_conversation(
    payload: ConversationCreate,
    current_user: CurrentUser = Depends(get_current_user)
):
    """
    Creates a new conversation thread for the user.
    """
    return ChatService.create_conversation(user_id=current_user.user_id, title=payload.title)

@router.get("/conversations/{id}/messages", response_model=List[MessageResponse])
async def get_messages(
    id: UUID,
    current_user: CurrentUser = Depends(get_current_user)
):
    """
    Retrieves historical messages for a specific conversation thread.
    """
    try:
        return ChatService.get_conversation_messages(user_id=current_user.user_id, conversation_id=id)
    except KeyError:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Conversation not found or access denied."
        )

@router.post("/conversations/{id}/messages")
async def send_message_stream(
    id: UUID,
    payload: MessageCreate,
    current_user: CurrentUser = Depends(get_current_user)
):
    """
    Posts a user message to the conversation and returns an asynchronous
    Server-Sent Events (SSE) stream delivering real-time tokens and safety status.
    """
    # 1. Rate Limit & Authorization Checks (executed before returning StreamingResponse)
    chat_rate_limiter.check_rate_limit(str(current_user.user_id))
    try:
        ChatService.validate_access(user_id=current_user.user_id, conversation_id=id)
    except KeyError:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Conversation not found or access denied."
        )

    event_stream = ChatService.process_message_stream(
        user_id=current_user.user_id,
        conversation_id=id,
        user_prompt=payload.content
    )
    return StreamingResponse(
        event_stream,
        media_type="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "Connection": "keep-alive",
            "X-Accel-Buffering": "no"
        }
    )

@router.post("/recommend", response_model=AIWorkoutRecommendation)
async def get_ai_workout_recommendation(
    payload: MessageCreate,
    current_user: CurrentUser = Depends(get_current_user)
):
    """
    Generates a structured, validated workout recommendation schema referencing
    real exercises from the catalog, strictly enforcing safety invariants.
    """
    try:
        return await ChatService.generate_workout_recommendation(
            user_id=current_user.user_id,
            prompt=payload.content
        )
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Workout recommendation failed: {str(e)}"
        )
