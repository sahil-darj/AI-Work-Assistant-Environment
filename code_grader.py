def grade_code(prediction: str, expected_keywords: list) -> float:
    """Keyword matching for code review grading."""
    score = 0.05
    for kw in expected_keywords:
        if kw.lower() in str(prediction).lower():
            score += 0.3
    return min(score, 0.95)
