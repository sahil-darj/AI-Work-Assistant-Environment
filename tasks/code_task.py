from pydantic import BaseModel
from typing import List

class CodeTask(BaseModel):
    id: str = "task_2"
    name: str = "Code Review"
    difficulty: str = "medium"
    description: str = "Identify the bug in the following Python code snippet."
    code_snippet: str
    expected_keywords: List[str]
    expected: List[str] = ["return", "result"] # Metadata alignment
    grader: str = "graders.code_grader.grade_code"

def get_code_tasks() -> List[CodeTask]:
    return [
        CodeTask(
            id="task_2",
            name="Code Review",
            difficulty="medium",
            code_snippet="def add(a, b):\n    result = a + b",
            expected_keywords=["return", "result"],
            expected=["return", "result"]
        )
    ]
