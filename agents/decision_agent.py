from typing import Dict, Optional


def assign_priority(task_text: str, deadline: Optional[str]) -> str:
    text = task_text.lower()

    if any(word in text for word in ["urgent", "immediately", "asap", "critical"]):
        return "high"
    if deadline:
        return "medium"
    return "low"


def assign_status(task: Dict) -> str:
    owner = task.get("owner")
    deadline = task.get("deadline")

    if not owner or not deadline:
        return "at_risk"
    return "ready"


def enrich_analysis(analysis: Dict) -> Dict:
    for task in analysis.get("tasks", []):
        if not task.get("priority"):
            task["priority"] = assign_priority(
                task.get("task", ""),
                task.get("deadline")
            )

        task["status"] = assign_status(task)

    return analysis