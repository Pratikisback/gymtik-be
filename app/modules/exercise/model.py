from sqlalchemy import String, Text, Float, Integer
from sqlalchemy.orm import Mapped, mapped_column
from pgvector.sqlalchemy import Vector

from app.db.base import Base


class Exercise(Base):
    __tablename__ = "exercises"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)

    title: Mapped[str] = mapped_column(String(255), nullable=False, index=True)

    description: Mapped[str] = mapped_column(Text, nullable=False)

    exercise_type: Mapped[str] = mapped_column(String(100), nullable=False)

    body_part: Mapped[str] = mapped_column(String(100), nullable=False, index=True)

    equipment: Mapped[str] = mapped_column(String(100), nullable=False)

    difficulty: Mapped[str] = mapped_column(String(50), nullable=False)

    rating: Mapped[float | None] = mapped_column(Float)

    rating_count: Mapped[int | None] = mapped_column(Integer)

    knowledge_document: Mapped[str] = mapped_column(Text, nullable=False)

    embedding: Mapped[list[float]] = mapped_column(Vector(768))