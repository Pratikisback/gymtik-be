from datetime import datetime

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.modules.auth.model import (
    EmailVerificationToken,
    RefreshToken,
)
from app.modules.user.model import User


class AuthRepository:
    def __init__(self, db: Session):
        self.db = db

    # ------------------------------------------------------------------
    # User
    # ------------------------------------------------------------------

    def get_user_by_email(
        self,
        email: str,
    ) -> User | None:
        return self.db.scalar(
            select(User).where(User.email == email)
        )

    def get_user_by_phone(
        self,
        phone_number: str,
    ) -> User | None:
        return self.db.scalar(
            select(User).where(User.phone_number == phone_number)
        )

    def get_user_by_id(
        self,
        user_id: int,
    ) -> User | None:
        return self.db.get(User, user_id)

    def create_user(
        self,
        user: User,
    ) -> User:
        self.db.add(user)
        self.db.flush()
        self.db.refresh(user)

        return user

    # ------------------------------------------------------------------
    # Email Verification
    # ------------------------------------------------------------------

    def create_verification_token(
        self,
        verification_token: EmailVerificationToken,
    ) -> EmailVerificationToken:
        self.db.add(verification_token)
        self.db.flush()

        return verification_token

    def get_verification_token(
        self,
        token: str,
    ) -> EmailVerificationToken | None:
        return self.db.scalar(
            select(EmailVerificationToken).where(
                EmailVerificationToken.token == token
            )
        )

    def delete_verification_token(
        self,
        verification_token: EmailVerificationToken,
    ) -> None:
        self.db.delete(verification_token)

    # ------------------------------------------------------------------
    # Refresh Token
    # ------------------------------------------------------------------

    def create_refresh_token(
        self,
        refresh_token: RefreshToken,
    ) -> RefreshToken:
        self.db.add(refresh_token)
        self.db.flush()

        return refresh_token

    def get_refresh_token(
        self,
        token_hash: str,
    ) -> RefreshToken | None:
        return self.db.scalar(
            select(RefreshToken).where(
                RefreshToken.token_hash == token_hash
            )
        )

    def delete_refresh_token(
        self,
        refresh_token: RefreshToken,
    ) -> None:
        self.db.delete(refresh_token)

    def delete_expired_refresh_tokens(
        self,
    ) -> None:
        expired_tokens = self.db.scalars(
            select(RefreshToken).where(
                RefreshToken.expires_at < datetime.now()
            )
        )

        for token in expired_tokens:
            self.db.delete(token)