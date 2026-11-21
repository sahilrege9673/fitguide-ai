from pydantic import BaseModel, Field
from typing import List, Optional
from uuid import UUID
from datetime import datetime, date
from app.schemas.exercise import ExerciseResponse

class ExerciseLogInput(BaseModel):
    session_exercise_id: UUID
    set_number: int = Field(..., ge=1)
    weight_kg: float = Field(default=0.0, ge=0.0)
    reps_performed: Optional[int] = Field(None, ge=1)
    duration_seconds: Optional[int] = Field(None, ge=1)
    rpe: Optional[int] = Field(None, ge=1, le=10)

class ExerciseLogResponse(BaseModel):
    id: UUID
    session_exercise_id: UUID
    user_id: UUID
    set_number: int
    weight_kg: float
    reps_performed: Optional[int] = None
    duration_seconds: Optional[int] = None
    rpe: Optional[int] = None
    logged_at: datetime

class SessionExerciseResponse(BaseModel):
    id: UUID
    session_id: UUID
    exercise_id: UUID
    exercise: ExerciseResponse
    exercise_order: int
    target_sets: int
    target_reps: Optional[int] = None
    target_duration_secs: Optional[int] = None
    target_rest_secs: int = 60
    is_completed: bool = False
    logs: List[ExerciseLogResponse] = Field(default_factory=list)

class WorkoutFeedbackInput(BaseModel):
    energy_rating: int = Field(..., ge=1, le=5)
    difficulty_rating: int = Field(..., ge=1, le=5)
    soreness_level: str
    user_comment: Optional[str] = None

class WorkoutFeedbackResponse(BaseModel):
    id: UUID
    session_id: UUID
    user_id: UUID
    energy_rating: int
    difficulty_rating: int
    soreness_level: str
    user_comment: Optional[str] = None
    created_at: datetime

class WorkoutSessionResponse(BaseModel):
    id: UUID
    user_id: UUID
    plan_id: Optional[UUID] = None
    title: str
    focus_area: str
    planned_duration_mins: int
    scheduled_time: Optional[datetime] = None
    completed_at: Optional[datetime] = None
    status: str
    perceived_exertion: Optional[int] = None
    notes: Optional[str] = None
    exercises: List[SessionExerciseResponse] = Field(default_factory=list)
    feedback: Optional[WorkoutFeedbackResponse] = None
    created_at: datetime

class GenerateWorkoutPlanRequest(BaseModel):
    cycle_type: str = "weekly"
    override_focus: Optional[str] = None

class CompleteSessionRequest(BaseModel):
    perceived_exertion: Optional[int] = Field(None, ge=1, le=10)
    notes: Optional[str] = None
    feedback: Optional[WorkoutFeedbackInput] = None

class SwapExerciseRequest(BaseModel):
    reason: Optional[str] = "joint_discomfort"
