import pytest

VALID_PAYLOAD = {
    "age_group": "adult_18_64",
    "experience_level": "intermediate",
    "fitness_goals": ["strength", "hypertrophy"],
    "workout_location": "commercial_gym",
    "available_equipment": ["barbell", "dumbbells", "bench"],
    "preferred_activities": ["weightlifting", "mobility"],
    "time_availability_mins": 45,
    "preferred_days": [1, 3, 5],
    "disclaimer_accepted": True
}

def test_get_onboarding_initially_empty(client, user_a_token):
    res = client.get("/api/v1/onboarding", headers={"Authorization": f"Bearer {user_a_token}"})
    assert res.status_code == 200
    assert res.json() is None

def test_save_onboarding_success(client, user_a_token, user_a_id):
    res = client.post(
        "/api/v1/onboarding",
        json=VALID_PAYLOAD,
        headers={"Authorization": f"Bearer {user_a_token}"}
    )
    assert res.status_code == 201
    data = res.json()
    assert data["user_id"] == str(user_a_id)
    assert data["age_group"] == "adult_18_64"
    assert data["time_availability_mins"] == 45
    assert data["disclaimer_accepted"] is True
    assert data["completed_at"] is not None

    # Check profile now reports has_completed_onboarding = True
    prof_res = client.get("/api/v1/auth/me", headers={"Authorization": f"Bearer {user_a_token}"})
    assert prof_res.status_code == 200
    assert prof_res.json()["has_completed_onboarding"] is True

def test_save_onboarding_disclaimer_required(client, user_a_token):
    invalid_payload = {**VALID_PAYLOAD, "disclaimer_accepted": False}
    res = client.post(
        "/api/v1/onboarding",
        json=invalid_payload,
        headers={"Authorization": f"Bearer {user_a_token}"}
    )
    # Pydantic field_validator rejects disclaimer_accepted=False with 422
    assert res.status_code == 422

def test_save_onboarding_invalid_duration(client, user_a_token):
    invalid_payload = {**VALID_PAYLOAD, "time_availability_mins": 5} # Below 10 mins minimum
    res = client.post(
        "/api/v1/onboarding",
        json=invalid_payload,
        headers={"Authorization": f"Bearer {user_a_token}"}
    )
    assert res.status_code == 422

def test_cross_user_isolation(client, user_a_token, user_b_token, user_a_id, user_b_id):
    # 1. User A saves preferences
    save_res = client.post(
        "/api/v1/onboarding",
        json=VALID_PAYLOAD,
        headers={"Authorization": f"Bearer {user_a_token}"}
    )
    assert save_res.status_code == 201

    # 2. User B requests onboarding preferences
    user_b_res = client.get(
        "/api/v1/onboarding",
        headers={"Authorization": f"Bearer {user_b_token}"}
    )
    assert user_b_res.status_code == 200
    # User B must get None, NOT User A's data!
    assert user_b_res.json() is None
