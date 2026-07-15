from pydantic import BaseModel

class ExerciseCSVRow(BaseModel):
    title: str
    description: str
    exercise_type: str
    body_part: str
    equipment: str
    difficulty: str
    rating: float | None = None
    rating_count: int | None = None
    

class ExerciseDocument(BaseModel):
    title: str
    description: str
    exercise_type: str
    body_part: str
    equipment: str
    difficulty: str
    knowledge_document: str | None = None
    rating: str | None = None
    embedding: list[float] | None = None