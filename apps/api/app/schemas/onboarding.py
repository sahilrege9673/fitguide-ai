from pydantic import BaseModel, Field, field_validator
from typing import List, Optional
from enum import Enum
from uuid import UUID
from datetime import datetime

class AgeGroup(str, Enum):
    MINOR_UNDER_18 = "minor_under_18"
    ADULT_18_64 = "adult_18_64"
    SENIOR_65_PLUS = "senior_65_plus"

class ExperienceLevel(str, Enum):
    BEGINNER = "beginner"
    INTERMEDIATE = "intermediate"
    ADVANCED = "advanced"

class OnboardingPreferencesInput(BaseModel):
    age_group: AgeGroup
    experience_level: ExperienceLevel
    fitness_goals: List[str] = Field(default_factory=list, min_length=1)
    workout_location: str = Field(..., min_length=2, max_length=100)
    available_equipment: List[str] = Field(default_factory=list)
    preferred_activities: List[str] = Field(default_factory=list)
    time_availability_mins: int = Field(..., ge=10, le=180)
    preferred_days: List[int] = Field(..., min_length=1, max_length=7)
    disclaimer_accepted: bool = Field(..., description="Must be True to complete onboarding")

    @field_validator("preferred_days")
    @classmethod
    def validate_days(cls, v: List[int]) -> List[int]:
        for day in v:
            if day < 1 or day > 7:
                raise ValueError("Preferred days must be integers between 1 (Monday) and 7 (Sunday).")
        return sorted(list(set(v)))

    @field_validator("disclaimer_accepted")
    @classmethod
    def validate_disclaimer(cls, v: bool) -> bool:
        if not v:
            raise ValueError("You must read and accept the fitness and health disclaimer to complete onboarding.")
        return v

class OnboardingPreferencesResponse(BaseModel):
    id: UUID
    user_id: UUID
    age_group: AgeGroup
    experience_level: ExperienceLevel
    fitness_goals: List[str]
    workout_location: str
    available_equipment: List[str]
    preferred_activities: List[str]
    time_availability_mins: int
    preferred_days: List[int]
    disclaimer_accepted: bool
    completed_at: Optional[datetime] = None
    created_at: datetime
    updated_at: datetime
