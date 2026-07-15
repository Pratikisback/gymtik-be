from fastapi import APIRouter

from app.api.v1.health import router as health_router
from app.modules.auth.router import router as auth_router
from app.modules.profile.router import router as profile_router
from app.modules.exercise.router import router as exercise_router
from app.modules.chat.router import router as chat_router

api_router = APIRouter()

api_router.include_router(health_router)
api_router.include_router(auth_router)
api_router.include_router(profile_router)
api_router.include_router(exercise_router)
api_router.include_router(chat_router)