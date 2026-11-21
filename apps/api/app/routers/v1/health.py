from fastapi import APIRouter
from datetime import datetime, timezone

router = APIRouter(tags=["Health"])

@router.get("/health")
def health_check():
    return {
        "status": "healthy",
        "service": "FeedGuide AI API",
        "version": "1.0.0",
        "timestamp": datetime.now(timezone.utc).isoformat()
    }

