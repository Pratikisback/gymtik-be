from app.modules.exercise.schemas import ExerciseDocument


class KnowledgeDocumentBuilder:

    def build(self, exercise: ExerciseDocument) -> str:
        sections = [
            f"Exercise Name:\n{exercise.title}",
            f"Description:\n{exercise.description}",
            f"Exercise Type:\n{exercise.exercise_type}",
            f"Primary Body Part:\n{exercise.body_part}",
            f"Equipment:\n{exercise.equipment}",
            f"Difficulty:\n{exercise.difficulty}",
        ]

        return "\n\n".join(sections)