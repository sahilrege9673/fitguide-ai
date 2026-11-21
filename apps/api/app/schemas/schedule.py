from pydantic import BaseModel
from typing import Optional
from uuid import UUID
from datetime import date, datetime

class ScheduleEntryResponse(BaseModel):
    id: UUID
    user_id: UUID
    session_id: Optional[UUID] = None
    scheduled_date: date
    entry_type: str
    title: str
    is_rest_day: bool
    is_completed: bool
    created_at: datetime

class RescheduleRequest(BaseModel):
    new_date: date
