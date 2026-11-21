from fastapi import APIRouter, Depends
from app.core.security import get_current_user, CurrentUser
from app.schemas.auth import UserProfileResponse
from app.services.profile_service import ProfileService

router = APIRouter(prefix="/auth", tags=["Authentication & Profile"])

@router.get("/me", response_model=UserProfileResponse)
def get_my_profile(current_user: CurrentUser = Depends(get_current_user)):
    """
    Returns the authenticated user's profile and onboarding completion state.
    Identity is derived strictly from verified Supabase JWT.
    """
    profile = ProfileService.get_or_create_profile(
        user_id=current_user.user_id,
        email=current_user.email,
        full_name=current_user.full_name
    )
    return profile
