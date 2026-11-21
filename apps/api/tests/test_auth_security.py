import pytest

def test_unauthenticated_request_rejected(client):
    response = client.get("/api/v1/auth/me")
    assert response.status_code == 401
    assert "detail" in response.json()

def test_invalid_token_rejected(client):
    response = client.get(
        "/api/v1/auth/me",
        headers={"Authorization": "Bearer invalid.token.value"}
    )
    assert response.status_code == 401

def test_expired_token_rejected(client, make_token, user_a_id):
    expired_token = make_token(user_a_id, expires_in_minutes=-10)
    response = client.get(
        "/api/v1/auth/me",
        headers={"Authorization": f"Bearer {expired_token}"}
    )
    assert response.status_code == 401
    assert "expired" in response.json()["detail"].lower()

def test_authenticated_profile_retrieval(client, user_a_token, user_a_id):
    response = client.get(
        "/api/v1/auth/me",
        headers={"Authorization": f"Bearer {user_a_token}"}
    )
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == str(user_a_id)
    assert data["email"] == "usera@example.com"
    assert data["has_completed_onboarding"] is False
