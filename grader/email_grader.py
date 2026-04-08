def grade_email(prediction: str, expected: str) -> float:
    """
    Grader for Email Triage Task.
    Correct -> 1.0, Incorrect -> 0.0
    """
    if prediction.strip().lower() == expected.strip().lower():
        return 1.0
    return 0.0
