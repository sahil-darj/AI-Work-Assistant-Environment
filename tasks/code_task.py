from pydantic import BaseModel
from typing import List

class CodeTask(BaseModel):
    id: str = "task_2"
    name: str = "Code Review"
    difficulty: str = "medium"
    description: str = "Identify the bug in the following Python code snippet."
    code_snippet: str
    expected_keywords: List[str]
    expected: str = "return, result" # Metadata alignment
    grader: str = "tasks.code_grader:grade_code"

def get_code_tasks() -> List[CodeTask]:
    return [
        CodeTask(
            id="task_2",
            name="Code Review",
            difficulty="medium",
            description="Identify the bug in the Python code snippet.",
            code_snippet="def add(a, b):\n    result = a + b",
            expected_keywords=["return", "result"],
            expected="return, result"
        )
    ]
