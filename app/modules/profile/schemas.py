from datetime import date
from typing import Literal

from pydantic import BaseModel, ConfigDict, Field

from app.shared.constants import (
    ActivityLevel,
    DietPreference,
    ExperienceLevel,
    FitnessGoal,
    Gender,
    WorkoutLocation,
)


class CreateProfileRequest(BaseModel):
    date_of_birth: date

    gender: Gender

    height_cm: float = Field(
        gt=0,
        le=300,
    )

    weight_kg: float = Field(
        gt=0,
        le=500,
    )

    fitness_goal: FitnessGoal

    activity_level: ActivityLevel

    experience_level: ExperienceLevel

    diet_preference: DietPreference

    workout_location: WorkoutLocation

    preferred_workout_duration_minutes: int = Field(
        ge=15,
        le=300,
    )

    workout_days_per_week: int = Field(
        ge=1,
        le=7,
    )

    preferred_workout_split: str = Field(
        min_length=2,
        max_length=100,
    )


class UpdateProfileRequest(BaseModel):
    date_of_birth: date | None = None

    gender: Gender | None = None

    height_cm: float | None = Field(
        default=None,
        gt=0,
        le=300,
    )

    weight_kg: float | None = Field(
        default=None,
        gt=0,
        le=500,
    )

    fitness_goal: FitnessGoal | None = None

    activity_level: ActivityLevel | None = None

    experience_level: ExperienceLevel | None = None

    diet_preference: DietPreference | None = None

    workout_location: WorkoutLocation | None = None

    preferred_workout_duration_minutes: int | None = Field(
        default=None,
        ge=15,
        le=300,
    )

    workout_days_per_week: int | None = Field(
        default=None,
        ge=1,
        le=7,
    )

    preferred_workout_split: str | None = Field(
        default=None,
        min_length=2,
        max_length=100,
    )


class ProfileResponse(BaseModel):
    model_config = ConfigDict(
        from_attributes=True,
    )

    id: int

    user_id: int

    date_of_birth: date

    gender: Gender

    height_cm: float

    weight_kg: float

    bmi: float

    fitness_goal: FitnessGoal

    activity_level: ActivityLevel

    experience_level: ExperienceLevel

    diet_preference: DietPreference

    workout_location: WorkoutLocation

    preferred_workout_duration_minutes: int

    workout_days_per_week: int

    preferred_workout_split: str