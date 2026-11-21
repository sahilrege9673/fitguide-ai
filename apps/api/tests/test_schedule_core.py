def test_schedule_retrieval_and_reschedule(client, user_a_token):
    # 1. Onboard user
    client.post(
        "/api/v1/onboarding",
        json={
            "age_group": "adult_18_64",
            "experience_level": "intermediate",
            "fitness_goals": ["hypertrophy"],
            "workout_location": "commercial_gym",
            "available_equipment": ["barbell", "dumbbells"],
            "preferred_activities": ["weightlifting"],
            "time_availability_mins": 45,
            "preferred_days": [1, 3, 5],
            "disclaimer_accepted": True
        },
        headers={"Authorization": f"Bearer {user_a_token}"}
    )

    # 2. Generate plan
    client.post(
        "/api/v1/workouts/generate",
        json={"cycle_type": "weekly"},
        headers={"Authorization": f"Bearer {user_a_token}"}
    )

    # 3. Get schedule
    res = client.get("/api/v1/schedule", headers={"Authorization": f"Bearer {user_a_token}"})
    assert res.status_code == 200
    entries = res.json()
    assert len(entries) == 7 # 7 days in the week

    first_entry = entries[0]
    entry_id = first_entry["id"]

    # 4. Reschedule entry
    patch_res = client.patch(
        f"/api/v1/schedule/{entry_id}/reschedule",
        json={"new_date": "2026-11-29"},
        headers={"Authorization": f"Bearer {user_a_token}"}
    )
    assert patch_res.status_code == 200
    assert patch_res.json()["scheduled_date"] == "2026-11-29"
