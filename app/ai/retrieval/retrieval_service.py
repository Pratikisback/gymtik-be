from sqlalchemy.ext.asyncio import AsyncSession

from app.ai.embeddings.embedding_service import EmbeddingService
from app.modules.exercise.repository import ExerciseRepository


class RetrievalService:

    def __init__(self):
        self.embedding_service = EmbeddingService()
        self.repository = ExerciseRepository()

    async def search(
        self,
        db: AsyncSession,
        question: str,
        top_k: int = 5,
    ):
        embedding = self.embedding_service.generate(question)

        return await self.repository.search_by_embedding(
            db=db,
            embedding=embedding,
            top_k=top_k,
        )