from pydantic import BaseModel
from typing import List, Any, Dict

class DataTask(BaseModel):
    id: str = "3"
    name: str = "Data Cleaning"
    difficulty: str = "hard"
    description: str = "Clean the provided messy dataset."
    messy_data: List[Dict[str, Any]]
    cleaned_data: List[Dict[str, Any]]
    expected: List[Dict[str, Any]] = [] # Metadata alignment
    grader: str = "data_grader:grade_data"

def get_data_tasks() -> List[DataTask]:
    expected_val = [{"id": 1, "name": "Alice", "age": 25}, {"id": 3, "name": "Charlie", "age": 30}]
    return [
        DataTask(
            id="task_3",
            name="Data Cleaning",
            difficulty="hard",
            description="Clean the messy dataset by fixing types and removing errors.",
            messy_data=[{"id": 1, "name": "Alice", "age": "25"}, {"id": 3, "name": "Charlie", "age": "30"}],
            cleaned_data=expected_val,
            expected=expected_val
        )
    ]
