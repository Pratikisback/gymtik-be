from fastapi import FastAPI
import app.db.models
from app.api.router import api_router
from app.core.config import settings
from app.core.lifespan import lifespan


app = FastAPI(
    title=settings.app.name,
    version=settings.app.version,
    debug=settings.is_development,
    lifespan=lifespan,
)

app.include_router(
    api_router,
    prefix=settings.app.api_v1_prefix,
)