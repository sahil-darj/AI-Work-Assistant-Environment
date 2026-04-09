from typing import List, Dict, Any

def grade_data(prediction: List[Dict[str, Any]], expected: List[Dict[str, Any]]) -> float:
    """Grades sorted data comparison with Phase 2 clamping (0.01, 0.99)."""
    if not isinstance(prediction, list):
        return 0.05
        
    try:
        # Sort both by 'id' to compare
        pred_sorted = sorted(prediction, key=lambda x: x.get('id', 0))
        exp_sorted = sorted(expected, key=lambda x: x.get('id', 0))
        
        if pred_sorted == exp_sorted:
            return 0.95
            
        # Check if at least some rows are cleaned
        correct_rows = 0
        exp_ids = {row.get('id') for row in exp_sorted}
        for row in pred_sorted:
            if row.get('id') in exp_ids and row in exp_sorted:
                correct_rows += 1
        
        if correct_rows > 0:
            return 0.5
            
    except Exception:
        return 0.05
        
    return 0.1
