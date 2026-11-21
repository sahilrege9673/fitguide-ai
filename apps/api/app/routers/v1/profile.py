from fastapi import APIRouter, Depends, HTTPException, status
from typing import Dict, Any
from datetime import datetime, timezone
from app.core.security import get_current_user, CurrentUser
from app.schemas.auth import UserProfileResponse
from app.schemas.profile import UpdateProfileRequest, UserDataExportResponse
from app.services.profile_service import ProfileService, _PROFILES_STORE, _PREFERENCES_STORE
from app.services.workout_service import WorkoutService, _SESSIONS_STORE, _SCHEDULE_STORE

router = APIRouter(prefix="/profile", tags=["Profile & Settings"])

@router.get("", response_model=UserProfileResponse)
def get_profile(current_user: CurrentUser = Depends(get_current_user)):
    return ProfileService.get_or_create_profile(
        user_id=current_user.user_id,
        email=current_user.email,
        full_name=current_user.full_name
    )

@router.patch("", response_model=UserProfileResponse)
def update_profile(
    payload: UpdateProfileRequest,
    current_user: CurrentUser = Depends(get_current_user)
):
    prof = ProfileService.get_or_create_profile(
        user_id=current_user.user_id,
        email=current_user.email,
        full_name=payload.full_name or current_user.full_name
    )
    return prof

@router.get("/export", response_model=UserDataExportResponse)
def export_user_data(current_user: CurrentUser = Depends(get_current_user)):
    """
    GDPR & CCPA Compliant Data Portability:
    Exports all personal profile records, onboarding preferences, workout sessions, and telemetry logs.
    """
    prof = ProfileService.get_or_create_profile(current_user.user_id, current_user.email)
    prefs = ProfileService.get_preferences(current_user.user_id)
    
    sessions = [s for s in _SESSIONS_STORE.values() if s["user_id"] == current_user.user_id]
    schedule = _SCHEDULE_STORE.get(current_user.user_id, [])

    return UserDataExportResponse(
        user_id=current_user.user_id,
        email=current_user.email,
        full_name=prof.full_name,
        exported_at=datetime.now(timezone.utc),
        profile=prof.model_dump(),
        onboarding_preferences=prefs.model_dump() if prefs else None,
        workout_sessions=[dict(s, id=str(s["id"]), user_id=str(s["user_id"])) for s in sessions],
        exercise_logs=[],
        schedule_entries=[dict(sc, id=str(sc["id"]), user_id=str(sc["user_id"])) for sc in schedule],
        feedback=[]
    )

@router.delete("", status_code=status.HTTP_204_NO_CONTENT)
def delete_user_account(current_user: CurrentUser = Depends(get_current_user)):
    """
    Cascade deletes all user records from the platform.
    """
    # Clean in-memory user records
    user_id = current_user.user_id
    if user_id in _PROFILES_STORE:
        del _PROFILES_STORE[user_id]
    if user_id in _PREFERENCES_STORE:
        del _PREFERENCES_STORE[user_id]
    if user_id in _SCHEDULE_STORE:
        del _SCHEDULE_STORE[user_id]

    # Remove user sessions
    keys_to_del = [sid for sid, s in _SESSIONS_STORE.items() if s["user_id"] == user_id]
    for sid in keys_to_del:
        del _SESSIONS_STORE[sid]

    return {}
