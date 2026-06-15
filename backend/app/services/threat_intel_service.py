import requests
from app.core.config import settings

class ThreatIntelService:
    def __init__(self):
        self.vt_api_key = settings.VIRUSTOTAL_API_KEY
        self.alienvault_api_key = settings.ALIENVAULT_API_KEY
        
    def lookup_ip(self, ip_address: str) -> dict:
        """
        Looks up an IP address in VirusTotal and AlienVault.
        """
        results = {"ip": ip_address, "virustotal": {}, "alienvault": {}}
        
        # Call to VirusTotal
        if self.vt_api_key:
            try:
                headers = {"x-apikey": self.vt_api_key}
                response = requests.get(f"https://www.virustotal.com/api/v3/ip_addresses/{ip_address}", headers=headers, timeout=10)
                if response.status_code == 200:
                    results["virustotal"] = response.json().get("data", {}).get("attributes", {}).get("last_analysis_stats", {})
            except Exception as e:
                print(f"VT Error: {e}")
                results["virustotal"] = {"error": str(e)}
        else:
            results["virustotal"] = {"error": "VIRUSTOTAL_API_KEY not configured."}
            
        # Call to AlienVault
        if self.alienvault_api_key:
            try:
                headers = {"X-OTX-API-KEY": self.alienvault_api_key}
                response = requests.get(f"https://otx.alienvault.com/api/v1/indicators/IPv4/{ip_address}/general", headers=headers, timeout=10)
                if response.status_code == 200:
                    results["alienvault"] = {"pulse_count": response.json().get("pulse_info", {}).get("count", 0)}
            except Exception as e:
                print(f"AlienVault Error: {e}")
                results["alienvault"] = {"error": str(e)}
        else:
            results["alienvault"] = {"error": "ALIENVAULT_API_KEY not configured."}
            
        return results
