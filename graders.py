from typing import List, Dict, Any

def grade_email(prediction: str, expected: str) -> float:
    """Simple binary grading for email triage."""
    score = 0.95 if str(prediction).lower().strip() == str(expected).lower().strip() else 0.05
    return max(min(score, 0.99), 0.01)

def grade_code(prediction: str, expected_keywords: list) -> float:
    """Keyword matching for code review grading."""
    score = 0.05
    for kw in expected_keywords:
        if str(kw).lower() in str(prediction).lower():
            score += 0.3
    return max(min(score, 0.99), 0.01)

def grade_data(prediction: List[Dict[str, Any]], expected: List[Dict[str, Any]]) -> float:
    """Grades sorted data comparison with Phase 2 clamping (0.01, 0.99)."""
    if not isinstance(prediction, list):
        return 0.01
        
    try:
        pred_sorted = sorted(prediction, key=lambda x: str(x.get('id', '0')))
        exp_sorted = sorted(expected, key=lambda x: str(x.get('id', '0')))
        
        if pred_sorted == exp_sorted:
            return 0.95
            
        correct_rows = 0
        exp_ids = {row.get('id') for row in exp_sorted}
        for row in pred_sorted:
            if row.get('id') in exp_ids and row in exp_sorted:
                correct_rows += 1
        
        if correct_rows > 0:
            return 0.5
            
    except Exception:
        return 0.01
        
    return 0.05
