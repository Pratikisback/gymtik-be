import secrets
from datetime import UTC, datetime, timedelta

from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.core.config import settings
from app.core.security import hash_password
from app.modules.auth.model import EmailVerificationToken
from app.modules.auth.repository import AuthRepository
from app.modules.auth.schemas import RegisterRequest, RegisterResponse, LoginRequest, TokenResponse
from app.modules.user.model import User
from app.tasks.email import send_email_task
import hashlib

from app.core.security import (
    create_access_token,
    create_refresh_token,
    verify_password,
)
from app.modules.auth.model import RefreshToken

class AuthService:
    def __init__(self, db: Session):
        self.db = db
        self.repository = AuthRepository(db)

    def register(
        self,
        request: RegisterRequest,
    ) -> RegisterResponse:

        if self.repository.get_user_by_email(request.email):
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Email already registered.",
            )

        if self.repository.get_user_by_phone(request.phone_number):
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Phone number already registered.",
            )

        user = User(
            first_name=request.first_name,
            middle_name=request.middle_name,
            last_name=request.last_name,
            email=request.email,
            phone_number=request.phone_number,
            password_hash=hash_password(request.password),
        )

        verification_token = EmailVerificationToken(
            token=secrets.token_urlsafe(32),
            expires_at=datetime.now(UTC)
            + timedelta(minutes=30),
        )

        try:
            user = self.repository.create_user(user)

            verification_token.user_id = user.id

            self.repository.create_verification_token(
                verification_token,
            )

            self.db.commit()

        except Exception:
            self.db.rollback()
            raise

        verification_url = (
            f"http://localhost:8000/api/v1/auth/verify-email"
            f"?token={verification_token.token}"
        )

        send_email_task.delay(
            to_email=user.email,
            subject="Verify your Gymtik account",
            body=(
                f"Hi {user.first_name},\n\n"
                f"Please verify your account by clicking the link below:\n\n"
                f"{verification_url}\n\n"
                f"This link is valid for 30 minutes."
            ),
        )

        return RegisterResponse(
            success=True,
            message=(
                "Registration successful. "
                "Please verify your email."
            ),
        )
        
    def verify_email(
        self,
        token: str,
    ):
        verification_token = self.repository.get_verification_token(
            token,
        )

        if verification_token is None:
            raise HTTPException(
                status_code=404,
                detail="Invalid verification token.",
            )

        if verification_token.expires_at < datetime.now(UTC):
            raise HTTPException(
                status_code=400,
                detail="Verification token has expired.",
            )

        user = self.repository.get_user_by_id(
            verification_token.user_id,
        )

        if user.is_verified:
            raise HTTPException(
                status_code=400,
                detail="User already verified.",
            )

        user.is_verified = True
        user.verified_at = datetime.now(UTC)

        self.repository.delete_verification_token(
            verification_token,
        )

        self.db.commit()

        return {
            "message": "Email verified successfully."
        } 
            
            
    def login(
        self,
        request: LoginRequest,
    ) -> TokenResponse:

        user = self.repository.get_user_by_email(
            request.email,
        )

        if user is None:
            raise HTTPException(
                status_code=401,
                detail="Invalid credentials.",
            )

        if not verify_password(
            request.password,
            user.password_hash,
        ):
            raise HTTPException(
                status_code=401,
                detail="Invalid credentials.",
            )

        if not user.is_verified:
            raise HTTPException(
                status_code=403,
                detail="Please verify your email first.",
            )

        access_token = create_access_token(
            user.id,
        )

        refresh_token = create_refresh_token(
            user.id,
        )

        refresh_token_model = RefreshToken(
            user_id=user.id,
            token_hash=hashlib.sha256(
                refresh_token.encode()
            ).hexdigest(),
            expires_at=datetime.now(UTC)
            + timedelta(
                days=settings.jwt.refresh_token_expiry_days,
            ),
        )

        self.repository.create_refresh_token(
            refresh_token_model,
        )

        self.db.commit()

        return TokenResponse(
            access_token=access_token,
            refresh_token=refresh_token,
        )
                
                
                