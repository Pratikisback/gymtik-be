from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.modules.exercise.model import Exercise


class ExerciseRepository:

    async def bulk_create(
        self,
        db: AsyncSession,
        exercises: list[Exercise],
    ) -> None:
        db.add_all(exercises)
        db.commit()
    
    async def search_by_embedding(
        self,
        db: AsyncSession,
        embedding: list[float],
        top_k: int = 5,
    ) -> list[Exercise]:

        stmt = (
            select(Exercise)
            .order_by(
                Exercise.embedding.cosine_distance(embedding)
            )
            .limit(top_k)
        )

        result = db.execute(stmt)

        return result.scalars().all()