import pytest
from datetime import date
from app.services.workout_service import WorkoutService

def test_unauthenticated_progress_access_rejected(client):
    res_summary = client.get("/api/v1/progress/summary")
    assert res_summary.status_code == 401

    res_pdf = client.get("/api/v1/progress/report/pdf")
    assert res_pdf.status_code == 401


def test_progress_summary_baseline_uncompleted(client, user_a_token):
    # Retrieve summary for user with no completed workouts yet
    res = client.get(
        "/api/v1/progress/summary?timeframe=30d",
        headers={"Authorization": f"Bearer {user_a_token}"}
    )
    assert res.status_code == 200
    data = res.json()
    assert data["timeframe"] == "30d"
    assert "start_date" in data
    assert "end_date" in data
    assert data["consistency_percentage"] >= 0.0
    assert data["completed_workouts"] == 0
    assert data["total_volume_kg"] == 0.0
    assert len(data["daily_activity"]) > 0
    assert "ai_insights" in data
    assert len(data["ai_insights"]) > 20


def test_progress_workflow_and_metrics_accumulation(client, user_a_token):
    # 1. Complete onboarding
    client.post(
        "/api/v1/onboarding",
        json={
            "age_group": "adult_18_64",
            "experience_level": "intermediate",
            "fitness_goals": ["strength", "hypertrophy"],
            "workout_location": "commercial_gym",
            "available_equipment": ["barbell", "dumbbells", "cable_machine", "bench"],
            "preferred_activities": ["weightlifting"],
            "time_availability_mins": 60,
            "preferred_days": [1, 2, 3, 4, 5, 6, 7],
            "disclaimer_accepted": True
        },
        headers={"Authorization": f"Bearer {user_a_token}"}
    )

    # 2. Generate workout plan
    gen_res = client.post(
        "/api/v1/workouts/generate",
        json={"cycle_type": "weekly"},
        headers={"Authorization": f"Bearer {user_a_token}"}
    )
    assert gen_res.status_code == 201
    sessions = gen_res.json()
    assert len(sessions) > 0

    first_session = sessions[0]
    session_id = first_session["id"]
    exercises = first_session["exercises"]
    assert len(exercises) > 0

    first_se = exercises[0]
    se_id = first_se["id"]

    # 3. Start workout session
    start_res = client.post(
        f"/api/v1/workouts/sessions/{session_id}/start",
        headers={"Authorization": f"Bearer {user_a_token}"}
    )
    assert start_res.status_code == 200

    # 4. Log 3 sets of 10 reps @ 60kg
    for s_idx in range(1, 4):
        log_res = client.post(
            f"/api/v1/workouts/sessions/{session_id}/log-exercise",
            json={
                "session_exercise_id": se_id,
                "set_number": s_idx,
                "weight_kg": 60.0,
                "reps_performed": 10,
                "rpe": 8
            },
            headers={"Authorization": f"Bearer {user_a_token}"}
        )
        assert log_res.status_code == 201

    # 5. Complete session
    comp_res = client.post(
        f"/api/v1/workouts/sessions/{session_id}/complete",
        json={
            "perceived_exertion": 8,
            "notes": "Solid hypertrophy session.",
            "feedback": {
                "energy_rating": 4,
                "difficulty_rating": 4,
                "soreness_level": "moderate"
            }
        },
        headers={"Authorization": f"Bearer {user_a_token}"}
    )
    assert comp_res.status_code == 200

    # 6. Check progress summary reflects completion and volume
    summary_res = client.get(
        "/api/v1/progress/summary?timeframe=7d",
        headers={"Authorization": f"Bearer {user_a_token}"}
    )
    assert summary_res.status_code == 200
    summary = summary_res.json()

    assert summary["completed_workouts"] >= 1
    # 3 sets * 10 reps * 60kg = 1800 kg
    assert summary["total_volume_kg"] >= 1800.0
    assert summary["total_reps"] >= 30
    assert summary["total_sets"] >= 3
    assert summary["total_active_mins"] > 0
    assert summary["streak_days"] >= 1
    assert len(summary["muscle_group_distribution"]) > 0

    # Check top muscle group has positive percentage
    top_muscle = summary["muscle_group_distribution"][0]
    assert top_muscle["percentage"] > 0
    assert top_muscle["sets"] >= 3
    assert top_muscle["volume_kg"] >= 1800.0

    # Check daily activity includes completed today
    today_str = date.today().strftime("%Y-%m-%d")
    today_acts = [d for d in summary["daily_activity"] if d["date"] == today_str]
    assert len(today_acts) == 1
    assert today_acts[0]["completed"] is True
    assert today_acts[0]["volume_kg"] >= 1800.0


def test_progress_pdf_generation(client, user_a_token):
    # Request downloadable PDF activity report
    pdf_res = client.get(
        "/api/v1/progress/report/pdf?timeframe=30d",
        headers={"Authorization": f"Bearer {user_a_token}"}
    )
    assert pdf_res.status_code == 200
    assert pdf_res.headers["content-type"] == "application/pdf"
    assert "attachment; filename=" in pdf_res.headers["content-disposition"]
    assert "fitguide-performance-report-30d.pdf" in pdf_res.headers["content-disposition"]

    pdf_bytes = pdf_res.content
    assert len(pdf_bytes) > 2000
    # Must start with standard PDF magic number '%PDF-'
    assert pdf_bytes.startswith(b"%PDF-")


def test_progress_timeframe_validation(client, user_a_token):
    for tf in ["7d", "30d", "90d", "all"]:
        res = client.get(
            f"/api/v1/progress/summary?timeframe={tf}",
            headers={"Authorization": f"Bearer {user_a_token}"}
        )
        assert res.status_code == 200

    # Invalid timeframe must fail validation with 422
    inv_res = client.get(
        "/api/v1/progress/summary?timeframe=invalid_tf",
        headers={"Authorization": f"Bearer {user_a_token}"}
    )
    assert inv_res.status_code == 422


def test_progress_user_isolation(client, user_a_token, user_b_token):
    # User B should have 0 completed workouts despite User A having completed sessions
    res_b = client.get(
        "/api/v1/progress/summary?timeframe=30d",
        headers={"Authorization": f"Bearer {user_b_token}"}
    )
    assert res_b.status_code == 200
    assert res_b.json()["completed_workouts"] == 0
    assert res_b.json()["total_volume_kg"] == 0.0
