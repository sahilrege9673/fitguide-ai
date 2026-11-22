from fastapi import FastAPI, Request, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from datetime import datetime, timezone

from app.core.config import settings
from app.routers.v1 import health, auth, onboarding, exercises, workouts, schedule, profile, chat, progress

app = FastAPI(
    title="FitGuide AI API",
    description="Engineered Fitness Companion API with strict safety guardrails and RLS isolation.",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# CORS Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Unified Error Handlers
@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    details = []
    for error in exc.errors():
        field = ".".join(str(loc) for loc in error.get("loc", []))
        details.append({
            "field": field,
            "issue": error.get("msg", "Validation error")
        })

    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content={
            "error": {
                "code": "VALIDATION_ERROR",
                "message": "The submitted payload failed data validation checks.",
                "details": details,
                "timestamp": datetime.now(timezone.utc).isoformat()
            }
        }
    )

# Mount Versioned Routers under /api/v1
app.include_router(health.router, prefix=settings.API_V1_PREFIX)
app.include_router(auth.router, prefix=settings.API_V1_PREFIX)
app.include_router(onboarding.router, prefix=settings.API_V1_PREFIX)
app.include_router(exercises.router, prefix=settings.API_V1_PREFIX)
app.include_router(workouts.router, prefix=settings.API_V1_PREFIX)
app.include_router(schedule.router, prefix=settings.API_V1_PREFIX)
app.include_router(profile.router, prefix=settings.API_V1_PREFIX)
app.include_router(chat.router, prefix=settings.API_V1_PREFIX)
app.include_router(progress.router, prefix=settings.API_V1_PREFIX)

@app.get("/")
def root():
    return {
        "service": "FitGuide AI API",
        "status": "operational",
        "api_docs": "/docs",
        "api_version": "v1"
    }
