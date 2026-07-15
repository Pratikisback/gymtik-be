from fastapi import (
    APIRouter,
    Depends,
    File,
    HTTPException,
    UploadFile,
)
from sqlalchemy.ext.asyncio import AsyncSession
import structlog
from app.ai.ingestion.ingestion_service import ExerciseIngestionService
from app.core.dependencies import get_exercise_ingestion_service
from app.db.database import get_db

logger = structlog.get_logger(__name__)
router = APIRouter(
    prefix="/exercises",
    tags=["Exercises"],
)


@router.post("/upload")
async def upload_exercises(
    file: UploadFile = File(...),
    db: AsyncSession = Depends(get_db),
    ingestion_service: ExerciseIngestionService = Depends(
        get_exercise_ingestion_service,
    ),
):
    
    if file.content_type != "text/csv":
        raise HTTPException(
            status_code=400,
            detail="Only CSV files are allowed.",
        )

    total_exercises = await ingestion_service.ingest(
        db=db,
        file=file,
    )

    return {
        "success": True,
        "message": "Exercises ingested successfully.",
        "total_exercises": total_exercises,
    }