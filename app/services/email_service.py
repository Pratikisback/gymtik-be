import smtplib

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from app.core.config import settings
from app.core.logger import logger

class EmailService:
    def __init__(self):
        self.host = settings.email.smtp_host
        self.port = settings.email.smtp_port
        self.username = settings.email.username
        self.password = settings.email.password
        self.enabled = settings.email.enabled

    def send_email(
        self,
        to_email: str,
        subject: str,
        body: str,
        is_html: bool = False,
    ) -> None:
        if not self.enabled:
            return

        message = MIMEMultipart()
        message["From"] = self.username
        message["To"] = to_email
        message["Subject"] = subject

        content_type = "html" if is_html else "plain"
        message.attach(MIMEText(body, content_type))

        with smtplib.SMTP(self.host, self.port) as smtp:
            smtp.starttls()
            smtp.login(self.username, self.password)
            smtp.send_message(message)
            logger.info("Email sent successfully to", email=to_email)

email_service = EmailService()



