def grade_code(prediction: str, expected: str) -> float:
    """
    Grader for Code Review Task.
    Exact match -> 1.0, Partially correct -> 0.5, Wrong -> 0.0
    """
    pred = prediction.strip().lower()
    exp = expected.strip().lower()
    
    if pred == exp:
        return 1.0
    
    # Partial match check (e.g., if agent provides explanation but contains keywords)
    if exp in pred:
        return 0.5
        
    return 0.0
