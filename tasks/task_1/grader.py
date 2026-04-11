def grade(prediction: str, expected: str) -> float:
    """Simple binary grading for email triage."""
    return 0.95 if prediction.lower() == expected.lower() else 0.05
