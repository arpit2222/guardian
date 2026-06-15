from app.agents import BaseAgent
from app.services.ml_service import SplunkMLService
from typing import Dict, Any
import json

class TriageAgent(BaseAgent):
    """
    TriageAgent receives the initial alert, extracts observables,
    and uses Splunk Hosted Models to determine severity and if investigation is needed.
    """
    def __init__(self):
        super().__init__()
        self.ml_service = SplunkMLService()

    def execute(self, context: Dict[str, Any]) -> Dict[str, Any]:
        result = context.get("result", {})
        
        # 1. Extract Observables (IPs, Users, Hashes)
        # In a real app, use regex to parse the raw log
        observables = {
            "src_ip": result.get("src_ip", result.get("src", "192.168.1.100")),
            "dest_ip": result.get("dest_ip", result.get("dest", "10.0.0.5")),
            "user": result.get("user", "admin")
        }
        
        # 2. Score Event with Splunk Foundation-Sec Model
        event_text = json.dumps(result)
        ml_analysis = self.ml_service.score_event(event_text)
        
        severity_score = ml_analysis.get("severity_score", 0)
        
        # 3. Decision
        requires_investigation = severity_score > 50
        
        return {
            "agent": self.name,
            "original_alert": context,
            "observables": observables,
            "ml_analysis": ml_analysis,
            "requires_investigation": requires_investigation,
            "triage_summary": f"Triage complete. Severity: {severity_score}. Proceeding to investigation: {requires_investigation}."
        }
