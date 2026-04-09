from pydantic import BaseModel
from typing import List

class CodeTask(BaseModel):
    id: str = "task_2"
    description: str = "Identify the bug in the following Python code snippet."
    code_snippet: str
    bug_type: str
    grader: str = "graders.code_grader.grade_code"

def get_code_tasks() -> List[CodeTask]:
    return [
        CodeTask(
            id="task_2_a",
            code_snippet="def add(a, b):\n    result = a + b",
            bug_type="missing return"
        )
    ]
