from pydantic import BaseModel
from typing import List

class CodeTask(BaseModel):
    id: str = "code-review"
    description: str = "Identify the bug in the following Python code snippet. State whether it's a 'missing return', 'wrong variable', or 'syntax error'."
    code_snippet: str
    bug_type: str

def get_code_tasks() -> List[CodeTask]:
    return [
        CodeTask(
            code_snippet="def add(a, b):\n    result = a + b",
            bug_type="missing return"
        ),
        CodeTask(
            code_snippet="def greet(name):\n    print('Hello ' + nmae)",
            bug_type="wrong variable"
        ),
        CodeTask(
            code_snippet="def check_even(n)\n    if n % 2 == 0:\n        return True",
            bug_type="syntax error"
        )
    ]
