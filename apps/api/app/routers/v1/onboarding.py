from fastapi import APIRouter, Depends, HTTPException, status
from typing import Optional
from app.core.security import get_current_user, CurrentUser
from app.schemas.onboarding import OnboardingPreferencesInput, OnboardingPreferencesResponse
from app.services.profile_service import ProfileService

router = APIRouter(prefix="/onboarding", tags=["Onboarding"])

@router.get("", response_model=Optional[OnboardingPreferencesResponse])
def get_onboarding_preferences(current_user: CurrentUser = Depends(get_current_user)):
    """
    Retrieves current user's onboarding preferences or returns null if not completed.
    """
    return ProfileService.get_preferences(current_user.user_id)

@router.post("", response_model=OnboardingPreferencesResponse, status_code=status.HTTP_201_CREATED)
def save_onboarding_preferences(
    payload: OnboardingPreferencesInput,
    current_user: CurrentUser = Depends(get_current_user)
):
    """
    Saves and persists user onboarding preferences.
    Requires accepted fitness disclaimer.
    """
    if not payload.disclaimer_accepted:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="You must accept the fitness and health safety disclaimer."
        )

    saved = ProfileService.save_preferences(
        user_id=current_user.user_id,
        payload=payload
    )
    return saved
