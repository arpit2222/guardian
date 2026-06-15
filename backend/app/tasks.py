from app.core.celery_app import celery_app
from app.agents.triage_agent import TriageAgent
from app.agents.investigate_agent import InvestigateAgent
from app.agents.remediate_agent import RemediateAgent
from app.core.config import settings
import time
import json
import redis

redis_client = redis.from_url(settings.REDIS_URL)

def process_splunk_alert(alert_data: dict):
    """
    Main orchestration task.
    Flow: Triage -> Investigate -> Remediate
    """
    try:
        # 1. TRIAGE
        # The triage agent performs initial categorization and extracts observables.
        triage_agent = TriageAgent()
        triage_result = triage_agent.execute(alert_data)
        
        if not triage_result.get("requires_investigation", False):
            return {"status": "resolved_at_triage", "details": triage_result}

        # 2. INVESTIGATE
        # The investigation agent looks up threat intel and queries Splunk for correlation.
        investigate_agent = InvestigateAgent()
        investigation_result = investigate_agent.execute(triage_result)

        # 3. REMEDIATE
        # The remediation agent decides on actions based on the investigation outcome.
        remediate_agent = RemediateAgent()
        remediation_result = remediate_agent.execute(investigation_result)

        final_report = {
            "id": alert_data.get("sid", f"SPL-{(int(time.time()))}"),
            "timestamp": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
            "source": alert_data.get("app", "Unknown Source"),
            "dest_ip": triage_result.get("observables", {}).get("dest_ip", "Unknown"),
            "src_ip": triage_result.get("observables", {}).get("src_ip", "Unknown"),
            "severity": triage_result.get("ml_analysis", {}).get("severity_score", 0),
            "status": "Remediated" if remediation_result.get("playbook_executed") != "False Positive Triage" else "Closed (False Positive)",
            "playbook": remediation_result.get("playbook_executed", "Unknown"),
            "triage": triage_result,
            "investigation": investigation_result,
            "remediation": remediation_result
        }
        
        # Save to Redis
        redis_client.lpush("recent_alerts", json.dumps(final_report))
        redis_client.ltrim("recent_alerts", 0, 99) # Keep latest 100

        return final_report
        
    except Exception as exc:
        print(f"Error processing alert: {exc}")
