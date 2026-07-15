from sqlalchemy.ext.asyncio import AsyncSession
from app.ai.llm.llm_service import LLMService
from app.ai.retrieval.retrieval_service import RetrievalService


class ChatService:

    def __init__(self):
        self.retrieval_service = RetrievalService()
        self.llm_service = LLMService()

    async def ask(
        self,
        db: AsyncSession,
        message: str,
    ):
        exercises = await self.retrieval_service.search(
            db=db,
            question=message,
        )

        answer = self.llm_service.generate(
            question=message,
            exercises=exercises,
        )

        return answer