from pydantic import BaseModel
from typing import List, Any, Dict

class DataTask(BaseModel):
    id: str = "task_3"
    description: str = "Clean the provided messy dataset."
    messy_data: List[Dict[str, Any]]
    cleaned_data: List[Dict[str, Any]]
    grader: str = "graders.data_grader.grade_data"

def get_data_tasks() -> List[DataTask]:
    return [
        DataTask(
            id="task_3_a",
            messy_data=[{"id": 1, "name": "Alice", "age": "25"}],
            cleaned_data=[{"id": 1, "name": "Alice", "age": 25}]
        )
    ]
