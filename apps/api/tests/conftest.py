import pytest
import jwt
from datetime import datetime, timedelta, timezone
from uuid import uuid4
from fastapi.testclient import TestClient
from main import app
from app.core.config import settings
from app.services.profile_service import ProfileService

@pytest.fixture(autouse=True)
def clean_database_store():
    ProfileService.clear_stores()
    yield
    ProfileService.clear_stores()

@pytest.fixture
def client():
    return TestClient(app)

@pytest.fixture
def user_a_id():
    return uuid4()

@pytest.fixture
def user_b_id():
    return uuid4()

@pytest.fixture
def make_token():
    def _generator(user_id, email="athlete@example.com", expires_in_minutes=60):
        payload = {
            "sub": str(user_id),
            "email": email,
            "role": "authenticated",
            "aud": "authenticated",
            "exp": datetime.now(timezone.utc) + timedelta(minutes=expires_in_minutes),
            "user_metadata": {
                "full_name": "Test Athlete"
            }
        }
        return jwt.encode(payload, settings.SUPABASE_JWT_SECRET, algorithm="HS256")
    return _generator

@pytest.fixture
def user_a_token(make_token, user_a_id):
    return make_token(user_a_id, email="usera@example.com")

@pytest.fixture
def user_b_token(make_token, user_b_id):
    return make_token(user_b_id, email="userb@example.com")
