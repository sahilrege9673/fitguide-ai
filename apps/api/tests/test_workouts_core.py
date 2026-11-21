from app.services.workout_service import WorkoutService

def test_generate_and_execute_workout_journey(client, user_a_token, user_a_id):
    WorkoutService.clear_stores()

    # 1. First complete onboarding
    onboard_res = client.post(
        "/api/v1/onboarding",
        json={
            "age_group": "adult_18_64",
            "experience_level": "intermediate",
            "fitness_goals": ["hypertrophy", "strength"],
            "workout_location": "commercial_gym",
            "available_equipment": ["barbell", "dumbbells", "cable_machine", "bench"],
            "preferred_activities": ["weightlifting"],
            "time_availability_mins": 45,
            "preferred_days": [1, 3, 5],
            "disclaimer_accepted": True
        },
        headers={"Authorization": f"Bearer {user_a_token}"}
    )
    assert onboard_res.status_code == 201

    # 2. Generate workout plan
    gen_res = client.post(
        "/api/v1/workouts/generate",
        json={"cycle_type": "weekly"},
        headers={"Authorization": f"Bearer {user_a_token}"}
    )
    assert gen_res.status_code == 201
    sessions = gen_res.json()
    assert len(sessions) == 3 # 3 active days: 1, 3, 5
    first_session = sessions[0]
    session_id = first_session["id"]
    assert len(first_session["exercises"]) >= 3

    # 3. Get today's workout
    today_res = client.get(
        "/api/v1/workouts/today",
        headers={"Authorization": f"Bearer {user_a_token}"}
    )
    assert today_res.status_code == 200
    assert today_res.json() is not None

    # 4. Start workout session
    start_res = client.post(
        f"/api/v1/workouts/sessions/{session_id}/start",
        headers={"Authorization": f"Bearer {user_a_token}"}
    )
    assert start_res.status_code == 200
    assert start_res.json()["status"] == "in_progress"

    # 5. Log exercise set
    target_se = first_session["exercises"][0]
    log_res = client.post(
        f"/api/v1/workouts/sessions/{session_id}/log-exercise",
        json={
            "session_exercise_id": target_se["id"],
            "set_number": 1,
            "weight_kg": 75.0,
            "reps_performed": 10,
            "rpe": 8
        },
        headers={"Authorization": f"Bearer {user_a_token}"}
    )
    assert log_res.status_code == 201
    assert log_res.json()["weight_kg"] == 75.0

    # 6. Swap an exercise with alternative
    swap_ex_id = first_session["exercises"][1]["exercise_id"]
    swap_res = client.post(
        f"/api/v1/workouts/sessions/{session_id}/exercises/{swap_ex_id}/swap",
        json={"reason": "joint_discomfort"},
        headers={"Authorization": f"Bearer {user_a_token}"}
    )
    assert swap_res.status_code == 200
    # Swapped exercise should have a new exercise ID
    updated_exercises = swap_res.json()["exercises"]
    assert any(se["exercise_id"] != swap_ex_id for se in updated_exercises)

    # 7. Complete workout session
    comp_res = client.post(
        f"/api/v1/workouts/sessions/{session_id}/complete",
        json={
            "perceived_exertion": 8,
            "notes": "Great session, chest felt engaged.",
            "feedback": {
                "energy_rating": 4,
                "difficulty_rating": 4,
                "soreness_level": "moderate",
                "user_comment": "Loved the exercise substitution."
            }
        },
        headers={"Authorization": f"Bearer {user_a_token}"}
    )
    assert comp_res.status_code == 200
    completed_session = comp_res.json()
    assert completed_session["status"] == "completed"
    assert completed_session["feedback"]["energy_rating"] == 4

    # 8. Check it appears in workout history
    hist_res = client.get(
        "/api/v1/workouts/history",
        headers={"Authorization": f"Bearer {user_a_token}"}
    )
    assert hist_res.status_code == 200
    assert len(hist_res.json()) >= 1
    assert hist_res.json()[0]["id"] == session_id
