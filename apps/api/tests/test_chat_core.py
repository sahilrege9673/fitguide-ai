import pytest
import json
from uuid import uuid4
from fastapi.testclient import TestClient

from app.services.profile_service import ProfileService
from app.schemas.onboarding import OnboardingPreferencesInput, AgeGroup, ExperienceLevel
from app.core.rate_limiter import chat_rate_limiter
from app.services.llm_service import llm_service, MockLLMProvider

@pytest.fixture(autouse=True)
def mock_llm_for_tests(monkeypatch):
    """Ensure tests run deterministically and instantaneously against MockLLMProvider."""
    monkeypatch.setattr(llm_service, "provider", MockLLMProvider())

@pytest.fixture
def test_user(make_token):
    user_id = uuid4()
    token = make_token(user_id, email=f"athlete_{user_id}@test.com")
    
    # Setup onboarding preferences for context
    prefs = OnboardingPreferencesInput(
        age_group=AgeGroup.ADULT_18_64,
        fitness_goals=["hypertrophy", "strength"],
        experience_level=ExperienceLevel.INTERMEDIATE,
        workout_location="commercial_gym",
        available_equipment=["barbell", "dumbbells", "bench"],
        preferred_activities=["weightlifting", "mobility"],
        time_availability_mins=45,
        preferred_days=[1, 3, 5],
        disclaimer_accepted=True
    )
    ProfileService.save_preferences(user_id, prefs)
    chat_rate_limiter.reset_for_user(str(user_id))
    
    return {"id": user_id, "token": token}


def test_create_and_list_conversations(client: TestClient, test_user):
    headers = {"Authorization": f"Bearer {test_user['token']}"}

    # 1. Create conversation
    create_resp = client.post(
        "/api/v1/chat/conversations",
        headers=headers,
        json={"title": "Bench Press Technique"}
    )
    assert create_resp.status_code == 201
    conv_data = create_resp.json()
    assert conv_data["title"] == "Bench Press Technique"
    conv_id = conv_data["id"]

    # 2. List conversations
    list_resp = client.get("/api/v1/chat/conversations", headers=headers)
    assert list_resp.status_code == 200
    threads = list_resp.json()
    assert len(threads) >= 1
    assert any(t["id"] == conv_id for t in threads)


def test_chat_streaming_safe_message(client: TestClient, test_user):
    headers = {"Authorization": f"Bearer {test_user['token']}"}

    # Create thread
    conv_resp = client.post("/api/v1/chat/conversations", headers=headers, json={})
    conv_id = conv_resp.json()["id"]

    # Send athletic question
    stream_resp = client.post(
        f"/api/v1/chat/conversations/{conv_id}/messages",
        headers=headers,
        json={"content": "What is an effective knee-friendly quad exercise?"}
    )
    assert stream_resp.status_code == 200
    assert "text/event-stream" in stream_resp.headers["content-type"]

    # Validate SSE events in payload
    content = stream_resp.text
    assert "event: meta" in content
    assert "event: token" in content
    assert "event: done" in content

    # Verify message was persisted
    history_resp = client.get(f"/api/v1/chat/conversations/{conv_id}/messages", headers=headers)
    assert history_resp.status_code == 200
    messages = history_resp.json()
    assert len(messages) == 2  # 1 user + 1 assistant
    assert messages[0]["sender_role"] == "user"
    assert messages[1]["sender_role"] == "assistant"


def test_safety_engine_intercepts_cardiac_red_flag(client: TestClient, test_user):
    headers = {"Authorization": f"Bearer {test_user['token']}"}

    # Create conversation
    conv_resp = client.post("/api/v1/chat/conversations", headers=headers, json={})
    conv_id = conv_resp.json()["id"]

    # Send critical red flag query
    stream_resp = client.post(
        f"/api/v1/chat/conversations/{conv_id}/messages",
        headers=headers,
        json={"content": "I feel sharp crushing chest pain and tightness while doing heavy sets. Should I push through?"}
    )
    assert stream_resp.status_code == 200
    content = stream_resp.text

    # Must emit safety stop and clinical directive
    assert "safety_stop" in content
    assert "cardiac_warning" in content
    assert "immediate clinical medical attention" in content or "emergency" in content


def test_safety_engine_minor_caloric_restriction(client: TestClient, make_token):
    # Setup minor athlete
    minor_id = uuid4()
    minor_token = make_token(minor_id, email="minor@example.com")
    prefs = OnboardingPreferencesInput(
        age_group=AgeGroup.MINOR_UNDER_18,
        fitness_goals=["strength"],
        experience_level=ExperienceLevel.BEGINNER,
        workout_location="home",
        available_equipment=["bodyweight"],
        preferred_activities=["bodyweight_training"],
        time_availability_mins=30,
        preferred_days=[2, 4],
        disclaimer_accepted=True
    )
    ProfileService.save_preferences(minor_id, prefs)
    chat_rate_limiter.reset_for_user(str(minor_id))

    headers = {"Authorization": f"Bearer {minor_token}"}
    conv_resp = client.post("/api/v1/chat/conversations", headers=headers, json={})
    conv_id = conv_resp.json()["id"]

    # Send minor calorie restriction prompt
    stream_resp = client.post(
        f"/api/v1/chat/conversations/{conv_id}/messages",
        headers=headers,
        json={"content": "How do I cut weight fast with a severe calorie deficit?"}
    )
    assert stream_resp.status_code == 200
    content = stream_resp.text
    assert "minor_caloric_restriction" in content or "safety_stop" in content


def test_structured_workout_recommendation_schema(client: TestClient, test_user):
    headers = {"Authorization": f"Bearer {test_user['token']}"}

    rec_resp = client.post(
        "/api/v1/chat/recommend",
        headers=headers,
        json={"content": "Generate a 45-minute upper body session focusing on chest and back"}
    )
    assert rec_resp.status_code == 200
    data = rec_resp.json()

    # Validate Pydantic schema keys
    assert "title" in data
    assert "focus_area" in data
    assert "estimated_duration_mins" in data
    assert "exercises" in data
    assert len(data["exercises"]) > 0

    first_ex = data["exercises"][0]
    assert "exercise_id" in first_ex
    assert "slug" in first_ex
    assert "name" in first_ex
    assert "target_sets" in first_ex
    assert "target_reps" in first_ex


def test_chat_rate_limiting(client: TestClient, test_user, monkeypatch):
    headers = {"Authorization": f"Bearer {test_user['token']}"}
    chat_rate_limiter.reset_for_user(str(test_user["id"]))
    monkeypatch.setattr(chat_rate_limiter, "limit", 3)

    conv_resp = client.post("/api/v1/chat/conversations", headers=headers, json={})
    conv_id = conv_resp.json()["id"]

    # First 3 requests should succeed
    for i in range(3):
        resp = client.post(
            f"/api/v1/chat/conversations/{conv_id}/messages",
            headers=headers,
            json={"content": f"Ping query {i}"}
        )
        assert resp.status_code == 200

    # 4th request must trigger 429
    rate_limited_resp = client.post(
        f"/api/v1/chat/conversations/{conv_id}/messages",
        headers=headers,
        json={"content": "Another query exceeding limit"}
    )
    assert rate_limited_resp.status_code == 429
    assert "Retry-After" in rate_limited_resp.headers
    assert rate_limited_resp.headers["X-RateLimit-Remaining"] == "0"
