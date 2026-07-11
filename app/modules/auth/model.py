from __future__ import annotations

from datetime import datetime
from typing import TYPE_CHECKING

from sqlalchemy import DateTime, ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base
from app.db.mixins import TimestampMixin

if TYPE_CHECKING:
    from app.modules.user.model import User


class EmailVerificationToken(Base, TimestampMixin):
    """
    Stores email verification tokens for newly registered users.
    """

    __tablename__ = "email_verification_tokens"

    id: Mapped[int] = mapped_column(
        primary_key=True,
    )

    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
    )

    token: Mapped[str] = mapped_column(
        String(255),
        unique=True,
        nullable=False,
        index=True,
    )

    expires_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
    )

    user: Mapped[User] = relationship(
        "User",
        back_populates="verification_tokens",
    )


class RefreshToken(Base, TimestampMixin):
    """
    Stores hashed refresh tokens for authenticated users.
    """

    __tablename__ = "refresh_tokens"

    id: Mapped[int] = mapped_column(
        primary_key=True,
    )

    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
    )

    token_hash: Mapped[str] = mapped_column(
        String(255),
        unique=True,
        nullable=False,
        index=True,
    )

    expires_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
    )

    device_name: Mapped[str | None] = mapped_column(
        String(255),
    )

    ip_address: Mapped[str | None] = mapped_column(
        String(45),
    )

    user: Mapped[User] = relationship(
        "User",
        back_populates="refresh_tokens",
    )