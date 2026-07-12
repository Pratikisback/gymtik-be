from __future__ import annotations

from datetime import date
from typing import TYPE_CHECKING

from sqlalchemy import Date, Float, ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base
from app.db.mixins import TimestampMixin
from app.shared.constants import (
    MAX_ACTIVITY_LEVEL_LENGTH,
    MAX_DIET_PREFERENCE_LENGTH,
    MAX_EXPERIENCE_LEVEL_LENGTH,
    MAX_GENDER_LENGTH,
    MAX_GOAL_LENGTH,
    MAX_WORKOUT_LOCATION_LENGTH,
    MAX_WORKOUT_SPLIT_LENGTH,
)

if TYPE_CHECKING:
    from app.modules.user.model import User


class UserProfile(Base, TimestampMixin):
    """
    Stores a user's fitness profile.
    """

    __tablename__ = "user_profiles"

    id: Mapped[int] = mapped_column(
        primary_key=True,
    )

    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"),
        unique=True,
        nullable=False,
    )

    # Personal
    date_of_birth: Mapped[date | None] = mapped_column(
        Date,
    )

    gender: Mapped[str | None] = mapped_column(
        String(MAX_GENDER_LENGTH),
    )

    # Body Metrics
    height_cm: Mapped[float | None] = mapped_column(
        Float,
    )

    weight_kg: Mapped[float | None] = mapped_column(
        Float,
    )

    bmi: Mapped[float | None] = mapped_column(
        Float,
    )

    # Fitness
    fitness_goal: Mapped[str | None] = mapped_column(
        String(MAX_GOAL_LENGTH),
    )

    activity_level: Mapped[str | None] = mapped_column(
        String(MAX_ACTIVITY_LEVEL_LENGTH),
    )

    experience_level: Mapped[str | None] = mapped_column(
        String(MAX_EXPERIENCE_LEVEL_LENGTH),
    )

    # Lifestyle
    diet_preference: Mapped[str | None] = mapped_column(
        String(MAX_DIET_PREFERENCE_LENGTH),
    )

    workout_location: Mapped[str | None] = mapped_column(
        String(MAX_WORKOUT_LOCATION_LENGTH),
    )

    preferred_workout_duration_minutes: Mapped[int | None] = mapped_column(
        Integer,
    )

    workout_days_per_week: Mapped[int | None] = mapped_column(
        Integer,
    )

    preferred_workout_split: Mapped[str | None] = mapped_column(
        String(MAX_WORKOUT_SPLIT_LENGTH),
    )

    # Relationships
    user: Mapped["User"] = relationship(
        "User",
        back_populates="profile",
    )