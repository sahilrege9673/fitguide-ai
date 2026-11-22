import json
import logging
import re
from typing import AsyncIterator, Dict, Any, List, Optional, Type
import httpx
from pydantic import BaseModel, ValidationError

from app.core.config import settings
from app.services.system_prompts import FITGUIDE_SYSTEM_PROMPT, WORKOUT_RECOMMENDATION_SYSTEM_PROMPT
from app.schemas.chat import AIWorkoutRecommendation, StructuredExerciseRef
from app.services.exercise_service import ExerciseService

logger = logging.getLogger(__name__)

class BaseLLMProvider:
    async def generate_text(self, prompt: str, system_instruction: str = FITGUIDE_SYSTEM_PROMPT, temperature: float = 0.7) -> str:
        raise NotImplementedError

    async def stream_text(self, prompt: str, system_instruction: str = FITGUIDE_SYSTEM_PROMPT, history: Optional[List[Dict[str, str]]] = None) -> AsyncIterator[str]:
        raise NotImplementedError

    async def generate_structured(self, prompt: str, schema_cls: Type[BaseModel] = AIWorkoutRecommendation, system_instruction: str = WORKOUT_RECOMMENDATION_SYSTEM_PROMPT) -> BaseModel:
        raise NotImplementedError


class MockLLMProvider(BaseLLMProvider):
    """
    Deterministic athletic coach provider for testing, offline use,
    and automatic fallback when external APIs are unreachable.
    """
    async def generate_text(self, prompt: str, system_instruction: str = FITGUIDE_SYSTEM_PROMPT, temperature: float = 0.7) -> str:
        lower = prompt.lower()
        if "knee" in lower or "squat" in lower:
            return (
                "### Knee-Friendly Quad Alternatives\n\n"
                "When experiencing patellofemoral pressure during deep knee flexion, prioritize movements with vertical shins or hip-dominant loading:\n\n"
                "1. **Spanish Squats or Box Squats**: Sit back deliberately into your hips, maintaining a vertical shin angle to deload the patellar tendon.\n"
                "2. **Reverse Lunges**: Decreases anterior knee shear compared to forward lunges. Take a slightly longer step and hinge slightly at the hip.\n"
                "3. **Romanian Deadlifts**: Shift emphasis to the posterior chain (hamstrings & glutes) to balance quadriceps dominance.\n\n"
                "*Coaching Note*: Work within a pain-free active range of motion and prioritize controlled eccentric tempos (3 seconds down)."
            )
        elif "recover" in lower or "rest" in lower or "mobility" in lower:
            return (
                "### Athletic Recovery Protocol\n\n"
                "Optimal recovery requires deliberate down-regulation and tissue restoration:\n\n"
                "- **Zone 1 Aerobic Flush**: 15–20 minutes of easy cycling or brisk walking to stimulate blood flow without autonomic fatigue.\n"
                "- **Thoracic & Hip Mobility**: 90/90 hip switches, cat-cow stretches, and world's greatest stretch (2 sets of 8 reps per side).\n"
                "- **Hydration & Electrolytes**: Ensure sodium, potassium, and magnesium replenishment alongside 2.5–3L of water.\n\n"
                "*Disclaimer*: FitGuide guidance is athletic in nature; if recovery issues are tied to injury, seek medical evaluation."
            )
        else:
            return (
                "### Athletic Guidance & Program Directives\n\n"
                f"Regarding your query: **{prompt[:80]}**\n\n"
                "- **Training Priority**: Emphasize movement quality, progressive overload, and full biomechanical range of motion.\n"
                "- **Load Management**: Track your Rate of Perceived Exertion (RPE 7–8 on primary working sets) leaving 1–2 reps in reserve (RIR).\n"
                "- **Execution**: Pair compound strength movements with targeted core and antagonist stabilizers.\n\n"
                "Stay disciplined, maintain consistent sleep hygiene, and log your completed sets."
            )

    async def stream_text(self, prompt: str, system_instruction: str = FITGUIDE_SYSTEM_PROMPT, history: Optional[List[Dict[str, str]]] = None) -> AsyncIterator[str]:
        full_text = await self.generate_text(prompt, system_instruction)
        # Yield words with small spaces to simulate realistic streaming
        tokens = full_text.split(" ")
        for i, token in enumerate(tokens):
            yield token + (" " if i < len(tokens) - 1 else "")

    async def generate_structured(self, prompt: str, schema_cls: Type[BaseModel] = AIWorkoutRecommendation, system_instruction: str = WORKOUT_RECOMMENDATION_SYSTEM_PROMPT) -> BaseModel:
        # Generate a validated recommendation pulling real exercises from catalog
        catalog = ExerciseService._build_catalog()
        selected = catalog[:4]
        exercise_refs = [
            StructuredExerciseRef(
                exercise_id=str(ex.id),
                slug=ex.slug,
                name=ex.name,
                category=ex.category,
                target_sets=3,
                target_reps="8-12",
                rest_seconds=90,
                coaching_cue=ex.instructions.split(".")[0] if ex.instructions else "Maintain neutral spine"
            )
            for ex in selected
        ]
        return AIWorkoutRecommendation(
            title="Balanced Athletic Conditioning Block",
            focus_area="Full Body Performance & Hypertrophy",
            estimated_duration_mins=45,
            rationale="Designed for athletic symmetry, progressive overload, and joint longevity based on your profile constraints.",
            exercises=exercise_refs,
            safety_advisories=[
                "Warm up thoroughly with dynamic mobility before starting working sets.",
                "Maintain core bracing (intra-abdominal pressure) during all compound movements."
            ]
        )


class GeminiProvider(BaseLLMProvider):
    """
    Direct Google Gemini REST client utilizing live streaming SSE endpoints.
    """
    def __init__(self, api_key: str, model: str = "gemini-3.5-flash-lite"):
        self.api_key = api_key
        self.model = model
        self.base_url = "https://generativelanguage.googleapis.com/v1beta/models"

    async def generate_text(self, prompt: str, system_instruction: str = FITGUIDE_SYSTEM_PROMPT, temperature: float = 0.7) -> str:
        url = f"{self.base_url}/{self.model}:generateContent?key={self.api_key}"
        payload = {
            "contents": [{"parts": [{"text": prompt}]}],
            "systemInstruction": {"parts": [{"text": system_instruction}]},
            "generationConfig": {
                "temperature": temperature,
                "maxOutputTokens": 1024
            }
        }
        async with httpx.AsyncClient(timeout=20.0) as client:
            resp = await client.post(url, json=payload)
            if resp.status_code != 200:
                raise RuntimeError(f"Gemini API returned status {resp.status_code}: {resp.text}")
            data = resp.json()
            candidates = data.get("candidates", [])
            if candidates and "content" in candidates[0]:
                parts = candidates[0]["content"].get("parts", [])
                return "".join([p.get("text", "") for p in parts])
            return ""

    async def stream_text(self, prompt: str, system_instruction: str = FITGUIDE_SYSTEM_PROMPT, history: Optional[List[Dict[str, str]]] = None) -> AsyncIterator[str]:
        url = f"{self.base_url}/{self.model}:streamGenerateContent?alt=sse&key={self.api_key}"
        
        # Build contents including historical turns if provided
        contents = []
        if history:
            for turn in history[-6:]:  # Keep recent context window
                role = "user" if turn.get("role") == "user" else "model"
                contents.append({"role": role, "parts": [{"text": turn.get("content", "")}]})
        contents.append({"role": "user", "parts": [{"text": prompt}]})

        payload = {
            "contents": contents,
            "systemInstruction": {"parts": [{"text": system_instruction}]},
            "generationConfig": {
                "temperature": 0.7,
                "maxOutputTokens": 1200
            }
        }

        async with httpx.AsyncClient(timeout=30.0) as client:
            async with client.stream("POST", url, json=payload) as response:
                if response.status_code != 200:
                    err_body = await response.aread()
                    raise RuntimeError(f"Gemini streaming failed ({response.status_code}): {err_body.decode('utf-8')}")

                async for line in response.aiter_lines():
                    if line.startswith("data:"):
                        json_str = line[5:].strip()
                        if not json_str:
                            continue
                        try:
                            chunk_data = json.loads(json_str)
                            candidates = chunk_data.get("candidates", [])
                            if candidates and "content" in candidates[0]:
                                parts = candidates[0]["content"].get("parts", [])
                                for p in parts:
                                    text_part = p.get("text")
                                    if text_part:
                                        yield text_part
                        except json.JSONDecodeError:
                            continue

    async def generate_structured(self, prompt: str, schema_cls: Type[BaseModel] = AIWorkoutRecommendation, system_instruction: str = WORKOUT_RECOMMENDATION_SYSTEM_PROMPT) -> BaseModel:
        # Prompt model with JSON instruction
        raw_output = await self.generate_text(
            prompt=f"{prompt}\n\nYou must reply ONLY with a valid JSON object matching the requested schema.",
            system_instruction=system_instruction,
            temperature=0.3
        )
        # Clean potential markdown fences ```json ... ```
        cleaned = re.sub(r"^```(?:json)?\s*", "", raw_output.strip())
        cleaned = re.sub(r"\s*```$", "", cleaned)

        try:
            parsed = json.loads(cleaned)
            return schema_cls(**parsed)
        except (json.JSONDecodeError, ValidationError) as e:
            logger.warning(f"Failed to parse structured LLM output ({e}). Falling back to deterministic repair.")
            # Fallback to Mock provider for guaranteed valid schema
            return await MockLLMProvider().generate_structured(prompt, schema_cls, system_instruction)


class LLMService:
    """
    Provider-agnostic facade. Defaults to live Gemini provider when GEMINI_API_KEY is configured;
    falls back cleanly to MockLLMProvider in offline/test environments.
    """
    def __init__(self, use_mock: bool = False):
        self.use_mock = use_mock
        if not use_mock and settings.GEMINI_API_KEY and settings.GEMINI_API_KEY.strip():
            self.provider: BaseLLMProvider = GeminiProvider(api_key=settings.GEMINI_API_KEY)
        else:
            self.provider = MockLLMProvider()

    async def generate_text(self, prompt: str, system_instruction: str = FITGUIDE_SYSTEM_PROMPT, temperature: float = 0.7) -> str:
        try:
            return await self.provider.generate_text(prompt, system_instruction, temperature)
        except Exception as e:
            logger.error(f"Primary LLM error ({e}), falling back to Mock provider.")
            return await MockLLMProvider().generate_text(prompt, system_instruction, temperature)

    async def stream_text(self, prompt: str, system_instruction: str = FITGUIDE_SYSTEM_PROMPT, history: Optional[List[Dict[str, str]]] = None) -> AsyncIterator[str]:
        try:
            async for chunk in self.provider.stream_text(prompt, system_instruction, history):
                yield chunk
        except Exception as e:
            logger.error(f"Streaming error ({e}), falling back to Mock provider.")
            async for chunk in MockLLMProvider().stream_text(prompt, system_instruction, history):
                yield chunk

    async def generate_workout_recommendation(self, prompt: str, user_context: str) -> AIWorkoutRecommendation:
        full_prompt = f"User Context:\n{user_context}\n\nUser Request: {prompt}"
        try:
            result = await self.provider.generate_structured(full_prompt, AIWorkoutRecommendation, WORKOUT_RECOMMENDATION_SYSTEM_PROMPT)
            return result  # type: ignore
        except Exception as e:
            logger.error(f"Workout recommendation error ({e}), falling back to Mock provider.")
            return await MockLLMProvider().generate_structured(full_prompt, AIWorkoutRecommendation, WORKOUT_RECOMMENDATION_SYSTEM_PROMPT)  # type: ignore

# Global singleton
llm_service = LLMService()
