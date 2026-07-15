import ollama

from app.ai.llm.prompt_builder import PromptBuilder
from app.modules.exercise.model import Exercise


class LLMService:

    def __init__(self):
        self.prompt_builder = PromptBuilder()

    def generate(
        self,
        question: str,
        exercises: list[Exercise],
    ) -> str:

        prompt = self.prompt_builder.build(
            question=question,
            exercises=exercises,
        )

        response = ollama.chat(
            model="qwen2.5:7b",
            messages=[
                {
                    "role": "user",
                    "content": prompt,
                }
            ],
        )

        return response["message"]["content"]