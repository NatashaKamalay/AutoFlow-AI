import json
import os
from datetime import datetime

AUDIT_PATH = "data/audit_log.json"


def log_event(agent_name: str, action: str, payload: dict):
    os.makedirs("data", exist_ok=True)

    if os.path.exists(AUDIT_PATH):
        try:
            with open(AUDIT_PATH, "r", encoding="utf-8") as f:
                logs = json.load(f)
        except json.JSONDecodeError:
            logs = []
    else:
        logs = []

    logs.append({
        "timestamp": datetime.utcnow().isoformat(),
        "agent": agent_name,
        "action": action,
        "payload": payload
    })

    with open(AUDIT_PATH, "w", encoding="utf-8") as f:
        json.dump(logs, f, indent=2)