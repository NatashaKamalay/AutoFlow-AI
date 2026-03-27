from typing import Dict, List


def monitor_tasks(analysis: Dict) -> Dict:
    risks: List[dict] = []

    tasks = analysis.get("tasks", [])

    for idx, task in enumerate(tasks, start=1):
        task_name = task.get("task", "Unnamed task")
        owner = task.get("owner")
        deadline = task.get("deadline")
        priority = task.get("priority", "low")

        if not owner:
            risks.append({
                "task_id": idx,
                "task": task_name,
                "risk_type": "missing_owner",
                "severity": "high",
                "message": f"Task '{task_name}' has no assigned owner."
            })

        if not deadline:
            risks.append({
                "task_id": idx,
                "task": task_name,
                "risk_type": "missing_deadline",
                "severity": "medium",
                "message": f"Task '{task_name}' has no deadline."
            })

        if priority == "high":
            risks.append({
                "task_id": idx,
                "task": task_name,
                "risk_type": "high_priority",
                "severity": "medium",
                "message": f"Task '{task_name}' is marked high priority."
            })

    return {
        "risk_count": len(risks),
        "risks": risks
    }