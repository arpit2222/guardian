from app.agents import BaseAgent
from app.services.threat_intel_service import ThreatIntelService
from app.services.splunk_service import SplunkService
from typing import Dict, Any

class InvestigateAgent(BaseAgent):
    """
    InvestigateAgent takes triage observables, enriches them with Threat Intel,
    and runs correlation searches in Splunk to find related activity.
    """
    def __init__(self):
        super().__init__()
        self.ti_service = ThreatIntelService()
        self.splunk_service = SplunkService()

    def execute(self, context: Dict[str, Any]) -> Dict[str, Any]:
        observables = context.get("observables", {})
        src_ip = observables.get("src_ip")
        
        # 1. Threat Intel Lookup
        ti_results = {}
        if src_ip:
            ti_results = self.ti_service.lookup_ip(src_ip)
            
        # 2. Splunk Correlation Search
        # Check if this IP has been seen attacking other hosts in the last 24h
        correlation_results = []
        if src_ip:
            query = f'search index=* src_ip="{src_ip}" | stats count by dest_ip, action'
            correlation_results = self.splunk_service.execute_search(query)
            
        # 3. Determine Risk Level based on TI and Correlation
        is_malicious = False
        vt_malicious = ti_results.get("virustotal", {}).get("malicious", 0)
        if vt_malicious > 0 or len(correlation_results) > 5:
            is_malicious = True
            
        return {
            "agent": self.name,
            "ti_enrichment": ti_results,
            "correlation_results": correlation_results,
            "is_malicious": is_malicious,
            "investigation_summary": f"Investigation complete. IP {src_ip} flagged as malicious: {is_malicious}."
        }
