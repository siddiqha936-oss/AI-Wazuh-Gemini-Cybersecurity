import json

with open("real_alert.json", "r") as file:
    alert = json.load(file)

agent = alert.get("agent", {})
rule = alert.get("rule", {})
event = alert.get("data", {}).get("win", {}).get("system", {})

level = int(rule.get("level", 0))
description = rule.get("description", "Unknown alert")
agent_name = agent.get("name", "Unknown")
rule_id = rule.get("id", "Unknown")
event_message = event.get("message", "No event message available")

if level >= 12:
    severity = "High"
elif level >= 7:
    severity = "Medium"
else:
    severity = "Low"

if level >= 12:
    actions = [
        "Notify the security analyst for urgent review.",
        "Review related alerts and activity on the endpoint.",
        "Follow the organization's approved incident-response procedure.",
        "Require human approval before taking any system-changing action."
    ]
elif level >= 7:
    actions = [
        "Review the alert and related events.",
        "Check whether the activity was expected.",
        "Monitor the endpoint for further suspicious activity.",
        "Escalate if supporting evidence indicates a threat."
    ]
else:
    actions = [
        "Record the alert for auditing.",
        "Check whether the activity was expected.",
        "Review nearby events for unusual activity.",
        "Continue monitoring the endpoint."
    ]

report = f"""
WAZUH INCIDENT RESPONSE RECOMMENDATION

Agent: {agent_name}
Rule ID: {rule_id}
Severity: {severity} (Wazuh level {level})
Alert: {description}

Event details:
{event_message}

Recommended actions:
""" + "\n".join(f"{i}. {action}" for i, action in enumerate(actions, 1))

report += "\n\nNote: Recommendations only. No system changes were made.\n"

print(report)

with open("incident_response.txt", "w") as file:
    file.write(report)

print("Report saved to incident_response.txt")
from datetime import datetime

with open("incident_audit.log", "a") as file:
    file.write(
        f"Time: {datetime.now().isoformat(timespec='seconds')}\n"
        f"Agent: {agent_name}\n"
        f"Rule ID: {rule_id}\n"
        f"Severity: {severity}\n"
        f"Alert: {description}\n"
        "------------------------------\n"
    )

print("Audit log updated: incident_audit.log")
