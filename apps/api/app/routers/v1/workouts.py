from fastapi import APIRouter, Depends, HTTPException, status, Header
from typing import List, Optional
from uuid import UUID
from app.core.security import get_current_user, CurrentUser
from app.schemas.workout import (
    WorkoutSessionResponse, ExerciseLogInput, ExerciseLogResponse,
    CompleteSessionRequest, GenerateWorkoutPlanRequest, SwapExerciseRequest
)
from app.services.workout_service import WorkoutService

router = APIRouter(prefix="/workouts", tags=["Workouts & Sessions"])

@router.post("/generate", response_model=List[WorkoutSessionResponse], status_code=status.HTTP_201_CREATED)
def generate_workout_plan(
    payload: GenerateWorkoutPlanRequest,
    current_user: CurrentUser = Depends(get_current_user)
):
    """
    Generates a tailored weekly workout plan based on the authenticated user's onboarding preferences.
    """
    try:
        sessions = WorkoutService.generate_weekly_plan(current_user.user_id)
        return sessions
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))

@router.get("/today", response_model=Optional[WorkoutSessionResponse])
def get_today_workout(current_user: CurrentUser = Depends(get_current_user)):
    """
    Retrieves today's prescribed workout session for the authenticated athlete.
    """
    return WorkoutService.get_today_session(current_user.user_id)

@router.get("/history", response_model=List[WorkoutSessionResponse])
def get_workout_history(current_user: CurrentUser = Depends(get_current_user)):
    """
    Retrieves completed workout session history for progress analytics.
    """
    return WorkoutService.get_history(current_user.user_id)

@router.get("/sessions/{id}", response_model=WorkoutSessionResponse)
def get_session_by_id(id: UUID, current_user: CurrentUser = Depends(get_current_user)):
    """
    Retrieves full details for a workout session including exercise sequence and logged sets.
    """
    session = WorkoutService.get_session_by_id(id, current_user.user_id)
    if not session:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Workout session not found.")
    return session

@router.post("/sessions/{id}/start", response_model=WorkoutSessionResponse)
def start_workout_session(id: UUID, current_user: CurrentUser = Depends(get_current_user)):
    """
    Transitions a workout session status to 'in_progress'.
    """
    try:
        return WorkoutService.start_session(id, current_user.user_id)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))

@router.post("/sessions/{id}/log-exercise", response_model=ExerciseLogResponse, status_code=status.HTTP_201_CREATED)
def log_exercise_set(
    id: UUID,
    payload: ExerciseLogInput,
    current_user: CurrentUser = Depends(get_current_user)
):
    """
    Logs an executed set (reps, weight, RPE, duration).
    """
    try:
        return WorkoutService.log_set(current_user.user_id, payload)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))

@router.post("/sessions/{id}/complete", response_model=WorkoutSessionResponse)
def complete_workout_session(
    id: UUID,
    payload: CompleteSessionRequest,
    idempotency_key: Optional[str] = Header(None),
    current_user: CurrentUser = Depends(get_current_user)
):
    """
    Completes a workout session and records post-workout feedback.
    """
    try:
        return WorkoutService.complete_session(id, current_user.user_id, payload)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))

@router.post("/sessions/{id}/exercises/{exercise_id}/swap", response_model=WorkoutSessionResponse)
def swap_exercise(
    id: UUID,
    exercise_id: UUID,
    payload: SwapExerciseRequest,
    current_user: CurrentUser = Depends(get_current_user)
):
    """
    Swaps an exercise in the session with a biologically and equipment-compatible alternative.
    """
    try:
        return WorkoutService.swap_exercise(id, current_user.user_id, exercise_id, payload.reason)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
