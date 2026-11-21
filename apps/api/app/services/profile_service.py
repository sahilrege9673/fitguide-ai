from typing import Optional, Dict, Any
from uuid import UUID, uuid4
from datetime import datetime, timezone
from app.schemas.onboarding import OnboardingPreferencesInput, OnboardingPreferencesResponse, AgeGroup, ExperienceLevel
from app.schemas.auth import UserProfileResponse

# In-memory persistence store for development / offline tests
# Mirrors Supabase public.profiles and public.onboarding_preferences
_PROFILES_STORE: Dict[UUID, Dict[str, Any]] = {}
_PREFERENCES_STORE: Dict[UUID, Dict[str, Any]] = {}

class ProfileService:
    @staticmethod
    def get_or_create_profile(user_id: UUID, email: str, full_name: Optional[str] = None) -> UserProfileResponse:
        now = datetime.now(timezone.utc)
        if user_id not in _PROFILES_STORE:
            _PROFILES_STORE[user_id] = {
                "id": user_id,
                "email": email,
                "full_name": full_name or "",
                "role": "user",
                "created_at": now,
                "updated_at": now
            }
        
        has_completed = user_id in _PREFERENCES_STORE and _PREFERENCES_STORE[user_id].get("completed_at") is not None
        prof = _PROFILES_STORE[user_id]
        return UserProfileResponse(
            id=prof["id"],
            email=prof["email"],
            full_name=prof["full_name"],
            role=prof["role"],
            has_completed_onboarding=has_completed,
            created_at=prof["created_at"]
        )

    @staticmethod
    def get_preferences(user_id: UUID) -> Optional[OnboardingPreferencesResponse]:
        if user_id not in _PREFERENCES_STORE:
            return None
        data = _PREFERENCES_STORE[user_id]
        return OnboardingPreferencesResponse(**data)

    @staticmethod
    def save_preferences(user_id: UUID, payload: OnboardingPreferencesInput) -> OnboardingPreferencesResponse:
        now = datetime.now(timezone.utc)
        existing = _PREFERENCES_STORE.get(user_id)
        
        pref_id = existing["id"] if existing else uuid4()
        created_at = existing["created_at"] if existing else now

        data = {
            "id": pref_id,
            "user_id": user_id,
            "age_group": payload.age_group,
            "experience_level": payload.experience_level,
            "fitness_goals": payload.fitness_goals,
            "workout_location": payload.workout_location,
            "available_equipment": payload.available_equipment,
            "preferred_activities": payload.preferred_activities,
            "time_availability_mins": payload.time_availability_mins,
            "preferred_days": payload.preferred_days,
            "disclaimer_accepted": payload.disclaimer_accepted,
            "completed_at": now if payload.disclaimer_accepted else None,
            "created_at": created_at,
            "updated_at": now
        }
        _PREFERENCES_STORE[user_id] = data
        return OnboardingPreferencesResponse(**data)

    @staticmethod
    def clear_stores():
        """Used in test fixtures for isolation"""
        _PROFILES_STORE.clear()
        _PREFERENCES_STORE.clear()
