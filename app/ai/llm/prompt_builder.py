from app.modules.exercise.model import Exercise


class PromptBuilder:

    def build(
        self,
        question: str,
        exercises: list[Exercise],
    ) -> str:

        context = "\n\n".join(
            exercise.knowledge_document
            for exercise in exercises
        )

        return f"""
            You are Gymtik, an AI fitness coach.

            Answer ONLY using the exercise knowledge below.

            If the answer cannot be determined from the provided knowledge, say so.

            ========================

            Exercise Knowledge

            {context}

            ========================

            User Question

            {question}

            Provide a practical, concise answer.
            """