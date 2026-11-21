from uuid import UUID
from typing import Optional, Dict, Any, List
from app.services.profile_service import ProfileService, _PROFILES_STORE
from app.services.workout_service import WorkoutService, _SESSIONS_STORE, _SCHEDULE_STORE

class ContextBuilder:
    """
    Constructs a token-efficient, prompt-injection-safe athletic context block
    summarizing the authenticated user's profile, onboarding preferences,
    and weekly training trajectory.
    """

    @classmethod
    def build_user_context(cls, user_id: UUID) -> str:
        lines: List[str] = []

        # 1. Profile & Identity
        user_prof = _PROFILES_STORE.get(user_id, {})
        full_name = user_prof.get("full_name") or "Athlete"
        lines.append(f"Athlete Name: {full_name}")

        # 2. Preferences & Physical Constraints
        prefs = ProfileService.get_preferences(user_id)
        if prefs:
            lines.append("### Onboarding Profile & Constraints")
            lines.append(f"- Age Group: {prefs.age_group.value}")
            lines.append(f"- Experience Level: {prefs.experience_level.value}")
            lines.append(f"- Fitness Goals: {', '.join(prefs.fitness_goals)}")
            lines.append(f"- Available Equipment: {', '.join(prefs.available_equipment) if prefs.available_equipment else 'Bodyweight only'}")
            loc = getattr(prefs, 'workout_location', None) or getattr(prefs, 'workout_locations', 'Standard Facility')
            if isinstance(loc, list):
                loc = ", ".join(loc)
            lines.append(f"- Workout Location: {loc}")
            days_str = ", ".join(str(d) for d in prefs.preferred_days) if prefs.preferred_days else "Flexible"
            lines.append(f"- Preferred Days: {days_str}")
            lines.append(f"- Session Time Limit: {prefs.time_availability_mins} minutes")
        else:
            lines.append("### Onboarding Profile")
            lines.append("- Status: Not yet completed. Adhere to conservative, safe baseline recommendations.")

        # 3. Schedule & Active Week
        schedule_entries = WorkoutService.get_schedule(user_id)
        if schedule_entries:
            lines.append("### Current Weekly Schedule")
            for entry in schedule_entries:
                is_comp = entry.get("is_completed", False)
                is_rest = entry.get("is_rest_day", False)
                status_tag = "[COMPLETED]" if is_comp else ("[REST]" if is_rest else "[SCHEDULED]")
                title = entry.get("title", "Training Session")
                s_date = entry.get("scheduled_date", "")
                lines.append(f"- {s_date}: {title} {status_tag}")
        else:
            lines.append("### Current Weekly Schedule")
            lines.append("- No active weekly plan generated yet.")

        # 4. Recent Completed Session History
        completed_sessions = [
            s for s in _SESSIONS_STORE.values()
            if s.get("user_id") == user_id and s.get("status") == "completed"
        ]
        if completed_sessions:
            lines.append("### Recent Completed Workouts")
            for sess in completed_sessions[-3:]:  # Last 3 completed sessions
                lines.append(f"- {sess.get('scheduled_date', '')}: {sess.get('title', '')} (Rating: {sess.get('perceived_exertion', 'N/A')}/10 RPE)")

        return "\n".join(lines)
