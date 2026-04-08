from pydantic import BaseModel
from typing import List, Dict, Any

class EmailTask(BaseModel):
    id: str = "email-triage"
    description: str = "Classify the following email text into one of: 'important', 'spam', or 'work'."
    email_text: str
    expected_category: str

def get_email_tasks() -> List[EmailTask]:
    return [
        EmailTask(
            email_text="Subject: Urgent: Q4 Project Update Required. Hi Team, please provide your updates by EOD.",
            expected_category="work"
        ),
        EmailTask(
            email_text="Congratulations!! You've won a $1000 gift card! Click here to claim your prize now!",
            expected_category="spam"
        ),
        EmailTask(
            email_text="Hi Sarah, are we still on for dinner tonight? My mom is coming over too.",
            expected_category="important"
        )
    ]
