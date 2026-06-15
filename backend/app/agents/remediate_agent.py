from app.agents import BaseAgent
from app.core.config import settings
from typing import Dict, Any
import datetime

class RemediateAgent(BaseAgent):
    """
    RemediateAgent takes the output of the investigation and determines
    which playbook to execute. It performs a mock execution for the hackathon.
    """
    def __init__(self):
        super().__init__()

    def execute(self, context: Dict[str, Any]) -> Dict[str, Any]:
        is_malicious = context.get("is_malicious", False)
        
        actions_taken = []
        
        if is_malicious:
            # Mock Remediations
            actions_taken.append({
                "action": "Block IP on Firewall",
                "target": "src_ip",
                "status": "Success",
                "timestamp": datetime.datetime.now().isoformat()
            })
            actions_taken.append({
                "action": "Isolate Endpoint",
                "target": "dest_ip",
                "status": "Pending Approval",
                "timestamp": datetime.datetime.now().isoformat()
            })
            playbook = "Ransomware Containment Playbook"
        else:
            actions_taken.append({
                "action": "Close Alert as False Positive",
                "status": "Success",
                "timestamp": datetime.datetime.now().isoformat()
            })
            playbook = "False Positive Triage"

        # Send Discord Notification if Webhook is configured
        if is_malicious and settings.DISCORD_WEBHOOK_URL:
            self._notify_discord(context, playbook)

        return {
            "agent": self.name,
            "playbook_executed": playbook,
            "actions_taken": actions_taken,
            "remediation_summary": f"Executed {playbook}. Actions: {len(actions_taken)}."
        }
        
    def _notify_discord(self, context: Dict[str, Any], playbook: str):
        import requests
        try:
            ip = context.get("observables", {}).get("src_ip", "Unknown")
            payload = {
                "content": "🚨 **CRITICAL SECURITY ALERT: SENTINEL AUTONOMOUS TRIAGE** 🚨",
                "embeds": [{
                    "title": f"Malicious Activity Detected from IP: {ip}",
                    "color": 15158332, # Red
                    "fields": [
                        {"name": "Playbook Initiated", "value": playbook, "inline": False},
                        {"name": "Severity", "value": str(context.get("ml_analysis", {}).get("severity_score", "Unknown")), "inline": True},
                        {"name": "Status", "value": "Awaiting Human Approval to Isolate", "inline": True}
                    ]
                }]
            }
            requests.post(settings.DISCORD_WEBHOOK_URL, json=payload, timeout=5)
        except Exception as e:
            print(f"Failed to send Discord notification: {e}")
