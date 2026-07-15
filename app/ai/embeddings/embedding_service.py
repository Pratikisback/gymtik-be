from langchain_ollama import OllamaEmbeddings

from app.core.config import get_settings


settings = get_settings()


class EmbeddingService:

    def __init__(self) -> None:
        self.embedding_model = OllamaEmbeddings(
            model=settings.ollama.embedding_model,
            base_url=settings.ollama.base_url,
        )

    def generate(self, text: str) -> list[float]:
        return self.embedding_model.embed_query(text)