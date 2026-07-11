from __future__ import annotations

from datetime import date
from typing import TYPE_CHECKING

from sqlalchemy import Date, Float, ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base
from app.db.mixins import TimestampMixin

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

    date_of_birth: Mapped[date | None] = mapped_column(
        Date,
    )

    gender: Mapped[str | None] = mapped_column(
        String(20),
    )

    height_cm: Mapped[float | None] = mapped_column(
        Float,
    )

    weight_kg: Mapped[float | None] = mapped_column(
        Float,
    )

    fitness_goal: Mapped[str | None] = mapped_column(
        String(100),
    )

    activity_level: Mapped[str | None] = mapped_column(
        String(50),
    )

    experience_level: Mapped[str | None] = mapped_column(
        String(50),
    )

    diet_preference: Mapped[str | None] = mapped_column(
        String(50),
    )

    user: Mapped[User] = relationship(
        "User",
        back_populates="profile",
    )