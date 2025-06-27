from typing import Any, Dict, List


def apply_feedback(facts: List[Dict[str, Any]], feedback: Dict[int, str]) -> List[Dict[str, Any]]:
    """Apply user feedback to a list of fact dictionaries."""
    processed: List[Dict[str, Any]] = []
    for idx, fact in enumerate(facts):
        action = feedback.get(idx, "accept")
        if action == "accept":
            processed.append(fact)
        elif action.startswith("edit:"):
            edited = fact.copy()
            edited["fact"] = action.split(":", 1)[1]
            processed.append(edited)
        # reject -> skip fact
    return processed
