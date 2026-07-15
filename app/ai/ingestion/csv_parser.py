from io import StringIO

import pandas as pd
from fastapi import UploadFile

from app.modules.exercise.schemas import ExerciseDocument


import pandas as pd




class CSVParser:
    REQUIRED_COLUMNS = {
        "Title",
        "Desc",
        "Type",
        "BodyPart",
        "Equipment",
        "Level",
    }
    
    def _clean_string(self, value) -> str:
        if pd.isna(value):
            return ""

        return str(value).strip()

    async def parse(self, file: UploadFile) -> list[ExerciseDocument]:
        content = await file.read()

        dataframe = pd.read_csv(StringIO(content.decode("utf-8")))

        missing_columns = self.REQUIRED_COLUMNS - set(dataframe.columns)

        if missing_columns:
            raise ValueError(
                f"Missing required columns: {', '.join(sorted(missing_columns))}"
            )

        exercises: list[ExerciseDocument] = []
        print(ExerciseDocument.model_fields.keys())
        for row in dataframe.itertuples(index=False):

            exercises.append(
                ExerciseDocument(
                    title=self._clean_string(row.Title),
                    description=self._clean_string(row.Desc),
                    exercise_type=self._clean_string(row.Type),
                    body_part=self._clean_string(row.BodyPart),
                    equipment=self._clean_string(row.Equipment),
                    difficulty=self._clean_string(row.Level),
                )
            )

        return exercises