from pydantic import BaseModel, EmailStr
from typing import Optional
from uuid import UUID
from datetime import datetime

class UserProfileResponse(BaseModel):
    id: UUID
    email: EmailStr
    full_name: Optional[str] = None
    role: str = "user"
    has_completed_onboarding: bool = False
    created_at: datetime
