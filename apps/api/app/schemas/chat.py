from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any
from datetime import datetime

class ConversationCreate(BaseModel):
    title: Optional[str] = Field(None, max_length=120, description="Initial conversation title")

class ConversationResponse(BaseModel):
    id: str
    user_id: str
    title: str
    created_at: str
    updated_at: str
    message_count: int = 0

class MessageCreate(BaseModel):
    content: str = Field(..., min_length=1, max_length=2000, description="User prompt text")

class CitationSource(BaseModel):
    title: str
    url: Optional[str] = None
    snippet: Optional[str] = None

class StructuredExerciseRef(BaseModel):
    exercise_id: str
    slug: str
    name: str
    category: str
    target_sets: int = 3
    target_reps: str = "8-12"
    rest_seconds: int = 90
    coaching_cue: Optional[str] = None

class AIWorkoutRecommendation(BaseModel):
    title: str
    focus_area: str
    estimated_duration_mins: int
    rationale: str
    exercises: List[StructuredExerciseRef]
    safety_advisories: List[str] = []

class MessageResponse(BaseModel):
    id: str
    conversation_id: str
    sender_role: str  # "user" | "assistant" | "system"
    content: str
    citations: Optional[List[CitationSource]] = None
    recommendation: Optional[AIWorkoutRecommendation] = None
    created_at: str

class ChatStreamEvent(BaseModel):
    event: str  # "meta" | "token" | "recommendation" | "error" | "done"
    data: Dict[str, Any]
