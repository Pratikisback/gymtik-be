from datetime import UTC, datetime, timedelta

import jwt
from pwdlib import PasswordHash

from app.core.config import settings


password_hash = PasswordHash.recommended()


def hash_password(password: str) -> str:
    return password_hash.hash(password)


def verify_password(
    plain_password: str,
    hashed_password: str,
) -> bool:
    return password_hash.verify(
        plain_password,
        hashed_password,
    )


def create_access_token(
    user_id: int,
) -> str:
    expires_at = datetime.now(UTC) + timedelta(
        minutes=settings.jwt.access_token_expiry_minutes,
    )

    payload = {
        "sub": str(user_id),
        "exp": expires_at,
        "type": "access",
    }

    return jwt.encode(
        payload,
        settings.jwt.secret_key,
        algorithm=settings.jwt.algorithm,
    )


def create_refresh_token(
    user_id: int,
) -> str:
    expires_at = datetime.now(UTC) + timedelta(
        days=settings.jwt.refresh_token_expiry_days,
    )

    payload = {
        "sub": str(user_id),
        "exp": expires_at,
        "type": "refresh",
    }

    return jwt.encode(
        payload,
        settings.jwt.secret_key,
        algorithm=settings.jwt.algorithm,
    )