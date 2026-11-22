from typing import Optional, Dict, Any
from uuid import UUID, uuid4
from datetime import datetime, timezone
import httpx
from app.core.config import settings
from app.schemas.onboarding import OnboardingPreferencesInput, OnboardingPreferencesResponse, AgeGroup, ExperienceLevel
from app.schemas.auth import UserProfileResponse

# In-memory persistence store for development / offline tests
# Mirrors Supabase public.profiles and public.onboarding_preferences
_PROFILES_STORE: Dict[UUID, Dict[str, Any]] = {}
_PREFERENCES_STORE: Dict[UUID, Dict[str, Any]] = {}

def _supabase_upsert(table: str, data: dict):
    if settings.SUPABASE_URL and not settings.SUPABASE_URL.startswith("https://mock") and settings.SUPABASE_SERVICE_ROLE_KEY:
        try:
            url = f"{settings.SUPABASE_URL.rstrip('/')}/rest/v1/{table}"
            headers = {
                "apikey": settings.SUPABASE_SERVICE_ROLE_KEY,
                "Authorization": f"Bearer {settings.SUPABASE_SERVICE_ROLE_KEY}",
                "Content-Type": "application/json",
                "Prefer": "resolution=merge-duplicates"
            }
            serializable = {}
            for k, v in data.items():
                if isinstance(v, UUID):
                    serializable[k] = str(v)
                elif isinstance(v, datetime):
                    serializable[k] = v.isoformat()
                else:
                    serializable[k] = v
            with httpx.Client(timeout=5.0) as client:
                client.post(url, json=[serializable], headers=headers)
        except Exception:
            pass

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
        _supabase_upsert("profiles", prof)
        return UserProfileResponse(
            id=prof["id"],
            email=prof["email"],
            full_name=prof["full_name"],
            role=prof["role"],
            has_completed_onboarding=has_completed,
            created_at=prof["created_at"]
        )

    @staticmethod
    def get_profile(user_id: UUID) -> Optional[UserProfileResponse]:
        if user_id not in _PROFILES_STORE:
            if settings.SUPABASE_URL and not settings.SUPABASE_URL.startswith("https://mock") and settings.SUPABASE_SERVICE_ROLE_KEY:
                try:
                    url = f"{settings.SUPABASE_URL.rstrip('/')}/rest/v1/profiles?id=eq.{user_id}&select=*"
                    headers = {
                        "apikey": settings.SUPABASE_SERVICE_ROLE_KEY,
                        "Authorization": f"Bearer {settings.SUPABASE_SERVICE_ROLE_KEY}"
                    }
                    with httpx.Client(timeout=5.0) as client:
                        res = client.get(url, headers=headers)
                        if res.status_code == 200:
                            rows = res.json()
                            if rows:
                                _PROFILES_STORE[user_id] = rows[0]
                except Exception:
                    pass

        if user_id not in _PROFILES_STORE:
            return None
        prof = _PROFILES_STORE[user_id]
        has_completed = user_id in _PREFERENCES_STORE and _PREFERENCES_STORE[user_id].get("completed_at") is not None
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
            if settings.SUPABASE_URL and not settings.SUPABASE_URL.startswith("https://mock") and settings.SUPABASE_SERVICE_ROLE_KEY:
                try:
                    url = f"{settings.SUPABASE_URL.rstrip('/')}/rest/v1/onboarding_preferences?user_id=eq.{user_id}&select=*"
                    headers = {
                        "apikey": settings.SUPABASE_SERVICE_ROLE_KEY,
                        "Authorization": f"Bearer {settings.SUPABASE_SERVICE_ROLE_KEY}"
                    }
                    with httpx.Client(timeout=5.0) as client:
                        res = client.get(url, headers=headers)
                        if res.status_code == 200:
                            rows = res.json()
                            if rows:
                                _PREFERENCES_STORE[user_id] = rows[0]
                except Exception:
                    pass

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
        _supabase_upsert("onboarding_preferences", data)
        return OnboardingPreferencesResponse(**data)

    @staticmethod
    def clear_stores():
        """Used in test fixtures for isolation"""
        _PROFILES_STORE.clear()
        _PREFERENCES_STORE.clear()
