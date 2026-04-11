from pydantic import BaseModel
from typing import List, Dict, Any

class EmailTask(BaseModel):
    id: str = "1"
    name: str = "Email Triage"
    difficulty: str = "easy"
    description: str = "Classify the following email text into one of: 'important', 'spam', or 'work'."
    email_text: str
    expected_category: str
    expected: str = "work" # Metadata alignment
    grader: str = "email_grader:grade_email"

def get_email_tasks() -> List[EmailTask]:
    return [
        EmailTask(
            id="task_1",
            name="Email Triage",
            difficulty="easy",
            description="Classify the email as spam, work, or important.",
            email_text="Subject: Urgent: Q4 Project Update Required.",
            expected_category="work",
            expected="work"
        )
    ]
