from celery import Celery

from app.core.config import settings


celery_app = Celery(
    "gymtik",
    broker=settings.redis.url,
    backend=settings.redis.url,
    include=["app.tasks.email"],
)

celery_app.conf.update(
    timezone="Asia/Kolkata",
    enable_utc=False,
    task_serializer="json",
    result_serializer="json",
    accept_content=["json"],
    task_track_started=True,
    task_time_limit=300,
    task_soft_time_limit=270,
)
