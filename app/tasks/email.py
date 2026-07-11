from app.celery.celery_app import celery_app
from app.services.email_service import email_service


@celery_app.task(name="tasks.send_email")
def send_email_task(
    to_email: str,
    subject: str,
    body: str,
    is_html: bool = False,
) -> None:
    email_service.send_email(
        to_email=to_email,
        subject=subject,
        body=body,
        is_html=is_html,
    )