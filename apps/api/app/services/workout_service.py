from typing import List, Optional, Dict, Any
from uuid import UUID, uuid4
from datetime import datetime, date, timedelta, timezone
from app.schemas.workout import (
    WorkoutSessionResponse, SessionExerciseResponse, ExerciseLogResponse,
    WorkoutFeedbackResponse, ExerciseLogInput, CompleteSessionRequest
)
from app.schemas.exercise import ExerciseResponse
from app.services.exercise_service import ExerciseService
from app.services.profile_service import ProfileService

# In-memory session store (synced with Supabase tables)
_PLANS_STORE: Dict[UUID, Dict[str, Any]] = {}
_SESSIONS_STORE: Dict[UUID, Dict[str, Any]] = {}
_LOGS_STORE: Dict[UUID, List[Dict[str, Any]]] = {} # session_exercise_id -> logs
_SCHEDULE_STORE: Dict[UUID, List[Dict[str, Any]]] = {} # user_id -> schedule entries

class WorkoutService:
    @classmethod
    def generate_weekly_plan(cls, user_id: UUID) -> List[WorkoutSessionResponse]:
        """
        Rule-based workout generator aware of age, equipment, time, and goals.
        Generates a 7-day periodized training block.
        """
        prefs = ProfileService.get_preferences(user_id)
        if not prefs:
            raise ValueError("Onboarding preferences must be completed before generating a workout plan.")

        age_group = prefs.age_group
        level = prefs.experience_level
        goals = prefs.fitness_goals
        equipment = prefs.available_equipment or ["bodyweight"]
        time_mins = prefs.time_availability_mins
        preferred_days = set(prefs.preferred_days)

        # Clear existing uncompleted scheduled sessions for user
        plan_id = uuid4()
        now = datetime.now(timezone.utc)
        today = date.today()
        # Start from Monday of the current week
        start_of_week = today - timedelta(days=today.weekday())

        generated_sessions = []
        schedule_entries = []

        # Split definitions based on number of active days
        split_themes = [
            ("Push & Upper Body", ["chest", "anterior_deltoids", "triceps"]),
            ("Pull & Back Mechanics", ["lats", "rhomboids", "biceps"]),
            ("Lower Body Posterior Chain", ["glutes", "hamstrings", "quadriceps"]),
            ("Full Body & Athletic Conditioning", ["quadriceps", "chest", "core", "lats"]),
            ("Upper Body Hypertrophy", ["chest", "lats", "lateral_deltoids"]),
            ("Legs & Core Stability", ["quadriceps", "hamstrings", "calves", "core"]),
            ("Aerobic Conditioning & Mobility", ["cardiovascular", "core", "mobility"])
        ]

        active_day_index = 0

        for day_offset in range(7):
            cur_date = start_of_week + timedelta(days=day_offset)
            day_num = cur_date.isoweekday() # 1 = Mon, 7 = Sun
            is_active = day_num in preferred_days

            if is_active:
                theme_title, target_muscles = split_themes[active_day_index % len(split_themes)]
                active_day_index += 1

                # Select exercises matching criteria
                selected_exercises = cls._select_exercises_for_session(
                    target_muscles=target_muscles,
                    age_group=age_group,
                    equipment=equipment,
                    time_mins=time_mins,
                    level=level
                )

                session_id = uuid4()
                session_exercises = []
                for order, ex in enumerate(selected_exercises, start=1):
                    se_id = uuid4()
                    # Age-appropriate sets/reps calibration
                    if age_group == "minor_under_18":
                        target_sets = 3
                        target_reps = 10
                        target_rest = 60
                    elif age_group == "senior_65_plus":
                        target_sets = 2
                        target_reps = 12
                        target_rest = 90
                    else:
                        target_sets = 4 if "strength" in goals else 3
                        target_reps = 6 if "strength" in goals and ex.category == "strength" else 10
                        target_rest = 75

                    se_data = {
                        "id": se_id,
                        "session_id": session_id,
                        "exercise_id": ex.id,
                        "exercise": ex,
                        "exercise_order": order,
                        "target_sets": target_sets,
                        "target_reps": target_reps,
                        "target_duration_secs": None,
                        "target_rest_secs": target_rest,
                        "is_completed": False,
                        "logs": []
                    }
                    session_exercises.append(se_data)

                session_data = {
                    "id": session_id,
                    "user_id": user_id,
                    "plan_id": plan_id,
                    "title": f"Day {day_num}: {theme_title}",
                    "focus_area": ", ".join(target_muscles[:2]).title(),
                    "planned_duration_mins": time_mins,
                    "scheduled_time": datetime.combine(cur_date, datetime.min.time()).replace(tzinfo=timezone.utc),
                    "completed_at": None,
                    "status": "scheduled",
                    "perceived_exertion": None,
                    "notes": f"Programmed for {level.capitalize()} ({age_group}).",
                    "exercises": session_exercises,
                    "feedback": None,
                    "created_at": now
                }
                _SESSIONS_STORE[session_id] = session_data
                generated_sessions.append(WorkoutSessionResponse(**session_data))

                schedule_entries.append({
                    "id": uuid4(),
                    "user_id": user_id,
                    "session_id": session_id,
                    "scheduled_date": cur_date,
                    "entry_type": "workout",
                    "title": theme_title,
                    "is_rest_day": False,
                    "is_completed": False,
                    "created_at": now
                })
            else:
                schedule_entries.append({
                    "id": uuid4(),
                    "user_id": user_id,
                    "session_id": None,
                    "scheduled_date": cur_date,
                    "entry_type": "rest_day",
                    "title": "Active Recovery & Mobility",
                    "is_rest_day": True,
                    "is_completed": False,
                    "created_at": now
                })

        _SCHEDULE_STORE[user_id] = schedule_entries
        return generated_sessions

    @classmethod
    def _select_exercises_for_session(
        cls,
        target_muscles: List[str],
        age_group: str,
        equipment: List[str],
        time_mins: int,
        level: str
    ) -> List[ExerciseResponse]:
        # Exercise count based on time availability
        if time_mins <= 20:
            count = 3
        elif time_mins <= 35:
            count = 4
        elif time_mins <= 50:
            count = 5
        else:
            count = 6

        catalog = ExerciseService._build_catalog()
        valid = []

        for e in catalog:
            # Must match age group
            if age_group not in e.suitable_age_groups:
                continue
            # Must match equipment or be bodyweight
            if e.equipment_needed and not any(eq in equipment or eq == "bodyweight" for eq in e.equipment_needed):
                continue
            # Match target muscles
            if any(tm in e.primary_muscles or tm in e.secondary_muscles for tm in target_muscles):
                valid.append(e)

        # Fallback if too few specific matches
        if len(valid) < count:
            fallback = [
                e for e in catalog 
                if age_group in e.suitable_age_groups 
                and (not e.equipment_needed or any(eq in equipment or eq == "bodyweight" for eq in e.equipment_needed))
            ]
            valid.extend([e for e in fallback if e not in valid])

        return valid[:count]

    @classmethod
    def get_today_session(cls, user_id: UUID) -> Optional[WorkoutSessionResponse]:
        today = date.today()
        # Find scheduled session for today or nearest upcoming
        for s in _SESSIONS_STORE.values():
            if s["user_id"] == user_id:
                s_date = s["scheduled_time"].date() if s["scheduled_time"] else None
                if s_date == today:
                    return WorkoutSessionResponse(**s)

        # If none exactly today, return the first scheduled session
        for s in _SESSIONS_STORE.values():
            if s["user_id"] == user_id and s["status"] in ("scheduled", "in_progress"):
                return WorkoutSessionResponse(**s)

        return None

    @classmethod
    def get_session_by_id(cls, session_id: UUID, user_id: UUID) -> Optional[WorkoutSessionResponse]:
        s = _SESSIONS_STORE.get(session_id)
        if s and s["user_id"] == user_id:
            return WorkoutSessionResponse(**s)
        return None

    @classmethod
    def start_session(cls, session_id: UUID, user_id: UUID) -> WorkoutSessionResponse:
        s = _SESSIONS_STORE.get(session_id)
        if not s or s["user_id"] != user_id:
            raise ValueError("Session not found or access denied.")
        s["status"] = "in_progress"
        return WorkoutSessionResponse(**s)

    @classmethod
    def log_set(cls, user_id: UUID, payload: ExerciseLogInput) -> ExerciseLogResponse:
        log_id = uuid4()
        now = datetime.now(timezone.utc)
        log_entry = {
            "id": log_id,
            "session_exercise_id": payload.session_exercise_id,
            "user_id": user_id,
            "set_number": payload.set_number,
            "weight_kg": payload.weight_kg,
            "reps_performed": payload.reps_performed,
            "duration_seconds": payload.duration_seconds,
            "rpe": payload.rpe,
            "logged_at": now
        }

        # Attach log to matching session exercise
        for s in _SESSIONS_STORE.values():
            if s["user_id"] == user_id:
                for se in s["exercises"]:
                    if se["id"] == payload.session_exercise_id:
                        se["logs"].append(log_entry)
                        # Mark completed if logged sets meet target sets
                        if len(se["logs"]) >= se["target_sets"]:
                            se["is_completed"] = True
                        return ExerciseLogResponse(**log_entry)

        raise ValueError("Session exercise not found.")

    @classmethod
    def complete_session(
        cls,
        session_id: UUID,
        user_id: UUID,
        payload: CompleteSessionRequest
    ) -> WorkoutSessionResponse:
        s = _SESSIONS_STORE.get(session_id)
        if not s or s["user_id"] != user_id:
            raise ValueError("Session not found or access denied.")

        now = datetime.now(timezone.utc)
        s["status"] = "completed"
        s["completed_at"] = now
        s["perceived_exertion"] = payload.perceived_exertion
        if payload.notes:
            s["notes"] = payload.notes

        if payload.feedback:
            fb = {
                "id": uuid4(),
                "session_id": session_id,
                "user_id": user_id,
                "energy_rating": payload.feedback.energy_rating,
                "difficulty_rating": payload.feedback.difficulty_rating,
                "soreness_level": payload.feedback.soreness_level,
                "user_comment": payload.feedback.user_comment,
                "created_at": now
            }
            s["feedback"] = fb

        # Mark matching schedule entry completed
        if user_id in _SCHEDULE_STORE:
            for entry in _SCHEDULE_STORE[user_id]:
                if entry.get("session_id") == session_id:
                    entry["is_completed"] = True

        return WorkoutSessionResponse(**s)

    @classmethod
    def swap_exercise(
        cls,
        session_id: UUID,
        user_id: UUID,
        exercise_id: UUID,
        reason: Optional[str] = None
    ) -> WorkoutSessionResponse:
        s = _SESSIONS_STORE.get(session_id)
        if not s or s["user_id"] != user_id:
            raise ValueError("Session not found.")

        prefs = ProfileService.get_preferences(user_id)
        age_group = prefs.age_group if prefs else "adult_18_64"
        equipment = prefs.available_equipment if prefs else ["bodyweight"]

        for se in s["exercises"]:
            if se["exercise_id"] == exercise_id:
                alt = ExerciseService.find_swap_alternative(se["exercise"], age_group, equipment)
                if alt:
                    se["exercise_id"] = alt.id
                    se["exercise"] = alt
                    se["logs"] = [] # Reset logs for swapped exercise
                    se["is_completed"] = False
                    return WorkoutSessionResponse(**s)

        raise ValueError("Could not find suitable swap alternative for this exercise.")

    @classmethod
    def get_history(cls, user_id: UUID) -> List[WorkoutSessionResponse]:
        completed = [
            WorkoutSessionResponse(**s) 
            for s in _SESSIONS_STORE.values() 
            if s["user_id"] == user_id and s["status"] == "completed"
        ]
        return sorted(completed, key=lambda x: x.completed_at or x.created_at, reverse=True)

    @classmethod
    def get_schedule(cls, user_id: UUID) -> List[Dict[str, Any]]:
        return _SCHEDULE_STORE.get(user_id, [])

    @classmethod
    def reschedule_entry(cls, user_id: UUID, entry_id: UUID, new_date: date) -> Dict[str, Any]:
        entries = _SCHEDULE_STORE.get(user_id, [])
        for e in entries:
            if e["id"] == entry_id:
                e["scheduled_date"] = new_date
                # If tied to a session, update scheduled_time
                if e.get("session_id") and e["session_id"] in _SESSIONS_STORE:
                    _SESSIONS_STORE[e["session_id"]]["scheduled_time"] = datetime.combine(new_date, datetime.min.time()).replace(tzinfo=timezone.utc)
                return e
        raise ValueError("Schedule entry not found.")

    @classmethod
    def clear_stores(cls):
        _PLANS_STORE.clear()
        _SESSIONS_STORE.clear()
        _LOGS_STORE.clear()
        _SCHEDULE_STORE.clear()
