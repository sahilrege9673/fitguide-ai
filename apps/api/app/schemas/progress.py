from typing import List, Optional, Dict
from pydantic import BaseModel, Field
from datetime import datetime
from enum import Enum

class TimeframeEnum(str, Enum):
    SEVEN_DAYS = "7d"
    THIRTY_DAYS = "30d"
    NINETY_DAYS = "90d"
    ALL_TIME = "all"

class DailyActivity(BaseModel):
    date: str
    day_name: str
    completed: bool
    workout_title: Optional[str] = None
    active_mins: int = 0
    volume_kg: float = 0.0
    sets_count: int = 0

class MuscleGroupVolume(BaseModel):
    muscle_group: str
    display_name: str
    sets: int
    volume_kg: float
    percentage: float

class ProgressSummaryResponse(BaseModel):
    timeframe: str
    start_date: str
    end_date: str
    consistency_percentage: float = Field(..., ge=0.0, le=100.0)
    completed_workouts: int = Field(..., ge=0)
    scheduled_workouts: int = Field(..., ge=0)
    total_volume_kg: float = Field(..., ge=0.0)
    total_active_mins: int = Field(..., ge=0)
    total_reps: int = Field(..., ge=0)
    total_sets: int = Field(..., ge=0)
    streak_days: int = Field(..., ge=0)
    muscle_group_distribution: List[MuscleGroupVolume]
    daily_activity: List[DailyActivity]
    ai_insights: str
    generated_at: datetime
