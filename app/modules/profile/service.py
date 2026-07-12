from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.modules.profile.model import UserProfile
from app.modules.profile.repository import (
    UserProfileRepository,
)
from app.modules.profile.schemas import (
    CreateProfileRequest,
    UpdateProfileRequest,
)
from app.modules.user.model import User


class UserProfileService:
    def __init__(
        self,
        db: Session,
    ):
        self.db = db
        self.repository = UserProfileRepository(db)

    def create_profile(
        self,
        user: User,
        request: CreateProfileRequest,
    ) -> UserProfile:

        if self.repository.exists(user.id):
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Profile already exists.",
            )

        profile = UserProfile(
            user_id=user.id,
            date_of_birth=request.date_of_birth,
            gender=request.gender,
            height_cm=request.height_cm,
            weight_kg=request.weight_kg,
            bmi=self._calculate_bmi(
                request.height_cm,
                request.weight_kg,
            ),
            fitness_goal=request.fitness_goal,
            activity_level=request.activity_level,
            experience_level=request.experience_level,
            diet_preference=request.diet_preference,
            workout_location=request.workout_location,
            preferred_workout_duration_minutes=request.preferred_workout_duration_minutes,
            workout_days_per_week=request.workout_days_per_week,
            preferred_workout_split=request.preferred_workout_split,
        )

        try:
            profile = self.repository.create(
                profile,
            )

            self.db.commit()

        except Exception:
            self.db.rollback()
            raise

        return profile

    def get_profile(
        self,
        user: User,
    ) -> UserProfile:

        profile = self.repository.get_by_user_id(
            user.id,
        )

        if profile is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Profile not found.",
            )

        return profile

    def update_profile(
        self,
        user: User,
        request: UpdateProfileRequest,
    ) -> UserProfile:

        profile = self.repository.get_by_user_id(
            user.id,
        )

        if profile is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Profile not found.",
            )

        update_data = request.model_dump(
            exclude_unset=True,
            exclude_none=True,
        )

        for field, value in update_data.items():
            setattr(
                profile,
                field,
                value,
            )

        if (
            profile.height_cm is not None
            and profile.weight_kg is not None
        ):
            profile.bmi = self._calculate_bmi(
                profile.height_cm,
                profile.weight_kg,
            )

        try:
            profile = self.repository.update(
                profile,
            )

            self.db.commit()

        except Exception:
            self.db.rollback()
            raise

        return profile

    @staticmethod
    def _calculate_bmi(
        height_cm: float,
        weight_kg: float,
    ) -> float:

        height_m = height_cm / 100

        return round(
            weight_kg / (height_m * height_m),
            2,
        )