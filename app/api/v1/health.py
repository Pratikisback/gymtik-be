from fastapi import APIRouter
from app.core.config import settings

router = APIRouter(tags=["Health"])

@router.get(
    "/health",
    summary="Health Check",
    description="Returns the current status of the application."
)
async def health_check():
    return {
        "status": "healthy",
        "application": settings.app.name,
        "version": settings.app.version,
        "environment": settings.app.env,
    }