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

        # Send Telegram Notification if configured
        if is_malicious and settings.TELEGRAM_BOT_TOKEN and settings.TELEGRAM_CHAT_ID:
            self._notify_telegram(context, playbook)

        return {
            "agent": self.name,
            "playbook_executed": playbook,
            "actions_taken": actions_taken,
            "remediation_summary": f"Executed {playbook}. Actions: {len(actions_taken)}."
        }
        
    def _notify_telegram(self, context: Dict[str, Any], playbook: str):
        import requests
        try:
            ip = context.get("observables", {}).get("src_ip", "Unknown")
            severity = str(context.get("ml_analysis", {}).get("severity_score", "Unknown"))
            
            message = (
                f"🚨 *CRITICAL SECURITY ALERT* 🚨\n\n"
                f"*Malicious Activity Detected from IP:* `{ip}`\n"
                f"*Severity Score:* {severity}\n"
                f"*Playbook Initiated:* {playbook}\n"
                f"*Status:* Awaiting Human Approval to Isolate"
            )
            
            url = f"https://api.telegram.org/bot{settings.TELEGRAM_BOT_TOKEN}/sendMessage"
            payload = {
                "chat_id": settings.TELEGRAM_CHAT_ID,
                "text": message,
                "parse_mode": "Markdown"
            }
            requests.post(url, json=payload, timeout=5)
        except Exception as e:
            print(f"Failed to send Telegram notification: {e}")
