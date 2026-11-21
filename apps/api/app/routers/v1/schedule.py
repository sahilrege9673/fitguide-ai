from fastapi import APIRouter, Depends, HTTPException, status
from typing import List, Dict, Any
from uuid import UUID
from app.core.security import get_current_user, CurrentUser
from app.schemas.schedule import RescheduleRequest
from app.services.workout_service import WorkoutService

router = APIRouter(prefix="/schedule", tags=["Schedule & Calendar"])

@router.get("", response_model=List[Dict[str, Any]])
def get_user_schedule(current_user: CurrentUser = Depends(get_current_user)):
    """
    Retrieves the 7-day schedule with workout and rest day entries.
    """
    return WorkoutService.get_schedule(current_user.user_id)

@router.patch("/{id}/reschedule", response_model=Dict[str, Any])
def reschedule_calendar_entry(
    id: UUID,
    payload: RescheduleRequest,
    current_user: CurrentUser = Depends(get_current_user)
):
    """
    Reschedules a workout or rest day to a new date.
    """
    try:
        return WorkoutService.reschedule_entry(current_user.user_id, id, payload.new_date)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
