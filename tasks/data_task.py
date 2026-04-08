from pydantic import BaseModel
from typing import List, Any, Dict

class DataTask(BaseModel):
    id: str = "data-cleaning"
    description: str = "Clean the provided messy dataset. You must: 1. Remove null values. 2. Correct data types (ensure 'age' is int). 3. Remove duplicates."
    messy_data: List[Dict[str, Any]]
    cleaned_data: List[Dict[str, Any]]

def get_data_tasks() -> List[DataTask]:
    return [
        DataTask(
            messy_data=[
                {"id": 1, "name": "Alice", "age": "25"},
                {"id": 2, "name": "Bob", "age": None},
                {"id": 1, "name": "Alice", "age": "25"},
                {"id": 3, "name": "Charlie", "age": 30.0}
            ],
            cleaned_data=[
                {"id": 1, "name": "Alice", "age": 25},
                {"id": 3, "name": "Charlie", "age": 30}
            ]
        )
    ]
