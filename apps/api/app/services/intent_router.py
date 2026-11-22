import os
import logging
from typing import Dict, Any, Optional
import joblib

logger = logging.getLogger(__name__)

CANDIDATE_PATHS = [
    os.environ.get("ML_ARTIFACT_PATH"),
    os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "..", "..", "ml", "artifacts", "baseline_classifier.joblib")),
    os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "ml_artifacts", "baseline_classifier.joblib")),
    os.path.abspath("/app/app/ml_artifacts/baseline_classifier.joblib"),
    os.path.abspath("/app/ml/artifacts/baseline_classifier.joblib"),
]
ARTIFACT_PATH = next((p for p in CANDIDATE_PATHS if p and os.path.exists(p)), CANDIDATE_PATHS[1])

ROUTING_TARGETS = {
    "safety_sensitive": "safety_intervene",
    "workout_request": "structured_workout_engine",
    "exercise_technique": "rag_knowledge_retrieval",
    "schedule_adjustment": "schedule_management",
    "progress_inquiry": "progress_analytics",
    "out_of_scope": "general_disclaimer_refusal"
}

class IntentRouterService:
    _MODEL = None

    @classmethod
    def get_model(cls):
        if cls._MODEL is None and os.path.exists(ARTIFACT_PATH):
            try:
                cls._MODEL = joblib.load(ARTIFACT_PATH)
                logger.info(f"Loaded ML Intent Classifier from {ARTIFACT_PATH}")
            except Exception as e:
                logger.error(f"Failed to load ML classifier: {e}")
        return cls._MODEL

    @classmethod
    def classify_intent(cls, query: str) -> Dict[str, Any]:
        """
        Classifies user query intent across 6 domain classes.
        Returns predicted intent, confidence score, and downstream routing target.
        """
        model = cls.get_model()
        clean_query = query.strip()
        if not clean_query:
            return {
                "intent": "out_of_scope",
                "confidence": 1.0,
                "routing_target": ROUTING_TARGETS["out_of_scope"]
            }

        if model is not None:
            try:
                pred = model.predict([clean_query])[0]
                probs = model.predict_proba([clean_query])[0]
                classes = list(model.classes_)
                confidence = float(probs[classes.index(pred)])
                return {
                    "intent": pred,
                    "confidence": round(confidence, 4),
                    "routing_target": ROUTING_TARGETS.get(pred, "general_dialogue")
                }
            except Exception as e:
                logger.warning(f"ML intent prediction failed: {e}")

        # Deterministic heuristic fallback
        lower = clean_query.lower()
        if any(w in lower for w in ["pain", "dizzy", "hurt", "swollen", "crushing", "faint", "doctor"]):
            intent = "safety_sensitive"
        elif any(w in lower for w in ["reschedule", "shift", "swap days", "rest day", "move to"]):
            intent = "schedule_adjustment"
        elif any(w in lower for w in ["how much", "progress", "streak", "volume", "history", "logged"]):
            intent = "progress_inquiry"
        elif any(w in lower for w in ["form", "technique", "cues", "difference between", "how deep", "tempo"]):
            intent = "exercise_technique"
        elif any(w in lower for w in ["workout", "routine", "exercises for", "plan", "train chest", "push day"]):
            intent = "workout_request"
        else:
            intent = "out_of_scope"

        return {
            "intent": intent,
            "confidence": 0.85,
            "routing_target": ROUTING_TARGETS.get(intent, "general_dialogue")
        }

intent_router = IntentRouterService()
