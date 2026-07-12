from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.core.dependencies import get_current_user
from app.db.database import get_db
from app.modules.profile.schemas import (
    CreateProfileRequest,
    ProfileResponse,
    UpdateProfileRequest,
)
from app.modules.profile.service import UserProfileService
from app.modules.user.model import User

router = APIRouter(
    prefix="/profile",
    tags=["Profile"],
)


@router.post(
    "",
    response_model=ProfileResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_profile(
    request: CreateProfileRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return UserProfileService(db).create_profile(
        current_user,
        request,
    )


@router.get(
    "",
    response_model=ProfileResponse,
)
def get_profile(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return UserProfileService(db).get_profile(
        current_user,
    )


@router.patch(
    "",
    response_model=ProfileResponse,
)
def update_profile(
    request: UpdateProfileRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return UserProfileService(db).update_profile(
        current_user,
        request,
    )