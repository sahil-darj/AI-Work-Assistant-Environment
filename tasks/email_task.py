from pydantic import BaseModel
from typing import List, Dict, Any

class EmailTask(BaseModel):
    id: str = "task_1"
    description: str = "Classify the following email text into one of: 'important', 'spam', or 'work'."
    email_text: str
    expected_category: str
    grader: str = "graders.email_grader.grade_email"

def get_email_tasks() -> List[EmailTask]:
    return [
        EmailTask(
            id="task_1_a",
            email_text="Subject: Urgent: Q4 Project Update Required.",
            expected_category="work"
        ),
        EmailTask(
            id="task_1_b",
            email_text="Congratulations!! You've won a $1000 gift card!",
            expected_category="spam"
        )
    ]
