from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.modules.auth.schemas import (
    LoginRequest,
    RegisterRequest,
    RegisterResponse,
    AccessTokenResponse,
    RefreshTokenRequest,
    TokenResponse,
)
from app.modules.auth.service import AuthService

router = APIRouter(
    prefix="/auth",
    tags=["Authentication"],
)


@router.post(
    "/register",
    response_model=RegisterResponse,
    status_code=201,
)
def register(
    request: RegisterRequest,
    db: Session = Depends(get_db),
):
    return AuthService(db).register(request)


@router.post("/verify-email")
def verify_email(
    token: str,
    db: Session = Depends(get_db),
):
    return AuthService(db).verify_email(token)


@router.post(
    "/login",
    response_model=TokenResponse,
)
def login(
    request: LoginRequest,
    db: Session = Depends(get_db),
):
    return AuthService(db).login(request)


@router.post(
    "/refresh",
    response_model=AccessTokenResponse,
)
def refresh_token(
    request: RefreshTokenRequest,
    db: Session = Depends(get_db),
):
    return AuthService(db).refresh_access_token(
        request.refresh_token,
    )