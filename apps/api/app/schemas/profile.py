from pydantic import BaseModel, EmailStr
from typing import Optional, Dict, Any, List
from uuid import UUID
from datetime import datetime
from app.schemas.onboarding import OnboardingPreferencesResponse

class UpdateProfileRequest(BaseModel):
    full_name: Optional[str] = None

class UserDataExportResponse(BaseModel):
    user_id: UUID
    email: str
    full_name: Optional[str]
    exported_at: datetime
    profile: Dict[str, Any]
    onboarding_preferences: Optional[Dict[str, Any]]
    workout_sessions: List[Dict[str, Any]]
    exercise_logs: List[Dict[str, Any]]
    schedule_entries: List[Dict[str, Any]]
    feedback: List[Dict[str, Any]]
