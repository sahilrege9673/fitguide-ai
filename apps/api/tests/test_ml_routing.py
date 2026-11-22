import os
import sys
import json

# Ensure project root is in sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "..")))

import pytest
from uuid import uuid4
from fastapi.testclient import TestClient

from app.services.intent_router import intent_router, ROUTING_TARGETS
from ml.train.train_lora import CLASSES

ML_DATA_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "..", "ml", "data"))
ML_ARTIFACTS_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "..", "ml", "artifacts"))

def test_ml_dataset_partition_and_balance():
    train_file = os.path.join(ML_DATA_DIR, "train.jsonl")
    val_file = os.path.join(ML_DATA_DIR, "val.jsonl")
    test_file = os.path.join(ML_DATA_DIR, "test.jsonl")

    assert os.path.exists(train_file), "train.jsonl must exist"
    assert os.path.exists(val_file), "val.jsonl must exist"
    assert os.path.exists(test_file), "test.jsonl must exist"

    train_data = [json.loads(line) for line in open(train_file, encoding="utf-8")]
    val_data = [json.loads(line) for line in open(val_file, encoding="utf-8")]
    test_data = [json.loads(line) for line in open(test_file, encoding="utf-8")]

    assert len(train_data) == 840
    assert len(val_data) == 180
    assert len(test_data) == 180

    # Test-set leakage verification
    train_texts = set(d["text"] for d in train_data)
    test_texts = set(d["text"] for d in test_data)
    leakage = train_texts.intersection(test_texts)
    assert len(leakage) == 0, f"Found {len(leakage)} overlapping samples between train and test splits!"


def test_baseline_model_artifact_load():
    model_path = os.path.join(ML_ARTIFACTS_DIR, "baseline_classifier.joblib")
    assert os.path.exists(model_path), "baseline_classifier.joblib artifact must exist"
    model = intent_router.get_model()
    assert model is not None
    assert hasattr(model, "predict")
    assert hasattr(model, "predict_proba")


def test_lora_model_artifact_load():
    lora_dir = os.path.join(ML_ARTIFACTS_DIR, "lora_model")
    config_file = os.path.join(lora_dir, "config.json")
    vocab_file = os.path.join(lora_dir, "vocab.json")
    weights_file = os.path.join(lora_dir, "best_lora_weights.pt")

    assert os.path.exists(config_file), "config.json must exist"
    assert os.path.exists(vocab_file), "vocab.json must exist"
    assert os.path.exists(weights_file), "best_lora_weights.pt must exist"

    with open(config_file, "r", encoding="utf-8") as f:
        config = json.load(f)
    assert config["rank"] == 16
    assert config["best_val_acc"] >= 0.95


@pytest.mark.parametrize("query,expected_intent", [
    ("Give me a 30-minute chest and triceps workout using dumbbells.", "workout_request"),
    ("What are the main coaching cues for proper Romanian deadlift mechanics?", "exercise_technique"),
    ("Can I reschedule my Monday workout to Friday evening?", "schedule_adjustment"),
    ("Show my total training volume and completed sets for the last month.", "progress_inquiry"),
    ("I felt a sharp crushing pain in my chest while lifting heavy weights.", "safety_sensitive"),
    ("What is the capital city of France?", "out_of_scope")
])
def test_intent_router_classifications(query, expected_intent):
    res = intent_router.classify_intent(query)
    assert res["intent"] == expected_intent
    assert res["confidence"] > 0.50
    assert res["routing_target"] == ROUTING_TARGETS[expected_intent]


def test_chat_classify_api_endpoint(client: TestClient, make_token):
    user_id = uuid4()
    token = make_token(user_id)
    headers = {"Authorization": f"Bearer {token}"}

    resp = client.post(
        "/api/v1/chat/classify",
        headers=headers,
        json={"content": "Can I move my Thursday leg session to Saturday?"}
    )
    assert resp.status_code == 200
    data = resp.json()
    assert data["intent"] == "schedule_adjustment"
    assert data["routing_target"] == "schedule_management"
    assert "confidence" in data
