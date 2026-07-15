from fastapi import UploadFile
from sqlalchemy.ext.asyncio import AsyncSession

from app.ai.embeddings.embedding_service import EmbeddingService
from app.ai.ingestion.csv_parser import CSVParser
from app.ai.ingestion.document_builder import KnowledgeDocumentBuilder
from app.modules.exercise.model import Exercise
from app.modules.exercise.repository import ExerciseRepository
import structlog

logger = structlog.get_logger(__name__)

class ExerciseIngestionService:

    def __init__(self):
        self.csv_parser = CSVParser()
        self.document_builder = KnowledgeDocumentBuilder()
        self.embedding_service = EmbeddingService()
        self.repository = ExerciseRepository()

    async def ingest(
        self,
        db: AsyncSession,
        file: UploadFile,
    ) -> int:

        logger.info("Starting parsing of the CSV into Exercise models")

        exercise_documents = await self.csv_parser.parse(file)

        exercise_models: list[Exercise] = []

        for document in exercise_documents:

            logger.info(
                "Creating knowledge document",
                exercise=document.title,
            )

            knowledge_document = self.document_builder.build(document)

            logger.info(
                "Generating embedding",
                exercise=document.title,
            )

            embedding = self.embedding_service.generate(
                knowledge_document
            )

            exercise = Exercise(
                title=document.title,
                description=document.description,
                exercise_type=document.exercise_type,
                body_part=document.body_part,
                equipment=document.equipment,
                difficulty=document.difficulty,
                rating=document.rating,
                knowledge_document=knowledge_document,
                embedding=embedding,
            )

            exercise_models.append(exercise)

        logger.info(
            "Bulk inserting exercises",
            total=len(exercise_models),
        )

        await self.repository.bulk_create(
            db=db,
            exercises=exercise_models,
        )

        return len(exercise_models)