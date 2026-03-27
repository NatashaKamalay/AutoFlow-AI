from typing import Dict, List


def generate_escalations(risk_report: Dict) -> Dict:
    escalations: List[dict] = []

    for risk in risk_report.get("risks", []):
        risk_type = risk["risk_type"]
        task = risk["task"]

        if risk_type == "missing_owner":
            escalations.append({
                "task": task,
                "action": "Request owner assignment",
                "level": "manager_review",
                "reason": "Execution cannot begin without ownership."
            })

        elif risk_type == "missing_deadline":
            escalations.append({
                "task": task,
                "action": "Request deadline clarification",
                "level": "team_followup",
                "reason": "Task progress cannot be monitored without a deadline."
            })

        elif risk_type == "high_priority":
            escalations.append({
                "task": task,
                "action": "Flag for immediate tracking",
                "level": "priority_watch",
                "reason": "High-priority tasks require closer monitoring."
            })

    return {
        "escalation_count": len(escalations),
        "escalations": escalations
    }