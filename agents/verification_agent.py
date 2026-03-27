from typing import Dict, List


def verify_analysis(analysis: Dict) -> Dict:
    issues: List[str] = []

    tasks = analysis.get("tasks", [])
    for idx, task in enumerate(tasks, start=1):
        if not task.get("owner"):
            issues.append(f"Task {idx} is missing an owner: {task.get('task')}")
        if not task.get("deadline"):
            issues.append(f"Task {idx} is missing a deadline: {task.get('task')}")
        if not task.get("task"):
            issues.append(f"Task {idx} has no task description.")

    if not analysis.get("summary"):
        issues.append("Summary is missing.")

    return {
        "is_valid": len(issues) == 0,
        "issues": issues
    }