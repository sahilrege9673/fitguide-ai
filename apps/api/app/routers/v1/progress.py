import io
import logging
from fastapi import APIRouter, Depends, Query, HTTPException, status
from fastapi.responses import StreamingResponse

from app.schemas.progress import ProgressSummaryResponse
from app.services.progress_service import ProgressService
from app.core.security import get_current_user, CurrentUser

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/progress", tags=["Progress & Analytics"])

@router.get("/summary", response_model=ProgressSummaryResponse)
async def get_progress_summary(
    timeframe: str = Query("30d", pattern="^(7d|30d|90d|all)$"),
    current_user: CurrentUser = Depends(get_current_user)
):
    """
    Retrieves weekly, monthly, or quarterly progress summary:
    consistency index, completed sessions, volume load (kg),
    active minutes, muscle group distribution, and AI insights.
    """
    try:
        summary = ProgressService.calculate_summary(
            user_id=current_user.user_id,
            timeframe=timeframe
        )
        return summary
    except Exception as e:
        logger.error(f"Error calculating progress summary for user {current_user.user_id}: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to generate progress analytics."
        )


@router.get("/report/pdf")
async def download_progress_pdf(
    timeframe: str = Query("30d", pattern="^(7d|30d|90d|all)$"),
    current_user: CurrentUser = Depends(get_current_user)
):
    """
    Generates and streams an authentic, publication-grade PDF activity report
    using ReportLab with Urban Performance aesthetics and grounded metrics.
    """
    try:
        pdf_bytes = ProgressService.generate_pdf_report(
            user_id=current_user.user_id,
            timeframe=timeframe
        )

        filename = f"fitguide-performance-report-{timeframe}.pdf"
        return StreamingResponse(
            io.BytesIO(pdf_bytes),
            media_type="application/pdf",
            headers={
                "Content-Disposition": f'attachment; filename="{filename}"',
                "Content-Length": str(len(pdf_bytes))
            }
        )
    except Exception as e:
        logger.error(f"Error generating PDF report for user {current_user.user_id}: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to generate PDF activity report: {str(e)}"
        )
