from fastapi import APIRouter, Query, HTTPException, status
from typing import Optional
from app.schemas.exercise import ExerciseListResponse, ExerciseResponse
from app.services.exercise_service import ExerciseService

router = APIRouter(prefix="/exercises", tags=["Exercise Library"])

@router.get("", response_model=ExerciseListResponse)
def get_exercises(
    category: Optional[str] = Query(None, description="Category filter (strength, hypertrophy, conditioning, mobility)"),
    difficulty: Optional[str] = Query(None, description="Difficulty filter (beginner, intermediate, advanced)"),
    muscle: Optional[str] = Query(None, description="Target muscle group filter"),
    equipment: Optional[str] = Query(None, description="Equipment required filter"),
    age_group: Optional[str] = Query(None, description="Age group filter"),
    search: Optional[str] = Query(None, description="Text search on name and instructions"),
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100)
):
    """
    Search and filter the authoritative exercise library (>= 80 verified exercises).
    Publicly accessible catalog with pagination.
    """
    return ExerciseService.list_exercises(
        category=category,
        difficulty=difficulty,
        muscle=muscle,
        equipment=equipment,
        age_group=age_group,
        search=search,
        page=page,
        page_size=page_size
    )

@router.get("/{slug}", response_model=ExerciseResponse)
def get_exercise_by_slug(slug: str):
    """
    Retrieves full details for a single exercise including form cues and cited demonstration media.
    """
    exercise = ExerciseService.get_by_slug(slug)
    if not exercise:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Exercise with slug '{slug}' was not found in the catalog."
        )
    return exercise
