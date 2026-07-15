from app.ai.embeddings.embedding_service import EmbeddingService

embedding_service = EmbeddingService()

embedding = embedding_service.generate(
    "Bench Press is a compound chest exercise."
)

print(len(embedding))