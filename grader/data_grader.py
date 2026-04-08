from typing import List, Dict, Any

def grade_data(prediction: List[Dict[str, Any]], expected: List[Dict[str, Any]]) -> float:
    """
    Grader for Data Cleaning Task.
    Fully correct -> 1.0, Partially cleaned -> 0.5, Incorrect -> 0.0
    """
    if not isinstance(prediction, list):
        return 0.0
        
    try:
        # Sort both by 'id' to compare
        pred_sorted = sorted(prediction, key=lambda x: x.get('id', 0))
        exp_sorted = sorted(expected, key=lambda x: x.get('id', 0))
        
        if pred_sorted == exp_sorted:
            return 1.0
            
        # Check if at least some rows are cleaned (simple heuristic)
        correct_rows = 0
        exp_ids = {row.get('id') for row in exp_sorted}
        for row in pred_sorted:
            if row.get('id') in exp_ids and row in exp_sorted:
                correct_rows += 1
        
        if correct_rows > 0:
            return 0.5
            
    except Exception:
        return 0.0
        
    return 0.0
