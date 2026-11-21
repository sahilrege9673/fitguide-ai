def test_profile_update_export_delete(client, user_a_token, user_a_id):
    # 1. Update Profile Name
    patch_res = client.patch(
        "/api/v1/profile",
        json={"full_name": "Jordan Champion"},
        headers={"Authorization": f"Bearer {user_a_token}"}
    )
    assert patch_res.status_code == 200
    assert patch_res.json()["full_name"] == "Jordan Champion"

    # 2. Export User Data Bundle
    export_res = client.get(
        "/api/v1/profile/export",
        headers={"Authorization": f"Bearer {user_a_token}"}
    )
    assert export_res.status_code == 200
    bundle = export_res.json()
    assert bundle["email"] == "usera@example.com"
    assert "profile" in bundle
    assert "workout_sessions" in bundle

    # 3. Delete Account
    del_res = client.delete(
        "/api/v1/profile",
        headers={"Authorization": f"Bearer {user_a_token}"}
    )
    assert del_res.status_code == 204
