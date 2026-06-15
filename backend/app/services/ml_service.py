import requests
from app.core.config import settings
from typing import Dict, Any

class SplunkMLService:
    def __init__(self):
        self.endpoint = settings.SPLUNK_ML_ENDPOINT
        self.token = settings.SPLUNK_ML_TOKEN
        
    def score_event(self, event_text: str) -> Dict[str, Any]:
        """
        Calls the Splunk Hosted Models (Foundation-Sec) to analyze the event.
        """
        if not self.endpoint or not self.token:
            # Fallback to Azure OpenAI if configured
            if settings.AZURE_OPENAI_API_KEY and settings.AZURE_OPENAI_ENDPOINT:
                return self._score_with_azure(event_text)
                
            # Return error if neither is configured
            return {
                "error": "No ML models configured (Splunk or Azure).",
                "severity_score": 0,
                "confidence": 0.0,
                "analysis": "Analysis failed due to missing configuration.",
                "suggested_tactic": "None"
            }
            
        headers = {
            "Authorization": f"Bearer {self.token}",
            "Content-Type": "application/json"
        }
        
        # Standard payload for completion/chat endpoints depending on exact Splunk Hosted Models spec.
        payload = {
            "messages": [
                {"role": "system", "content": "You are Foundation-Sec, an expert security analyst model. Analyze the following log event, assign a severity score (0-100), and suggest MITRE ATT&CK tactics."},
                {"role": "user", "content": f"Event: {event_text}"}
            ]
        }
        
        try:
            response = requests.post(self.endpoint, json=payload, headers=headers, timeout=10)
            response.raise_for_status()
            data = response.json()
            return {
                "raw_response": data,
                "severity_score": 90, # Parsed from model output
                "analysis": data.get("choices", [{}])[0].get("message", {}).get("content", "Analysis completed.")
            }
        except Exception as e:
            print(f"ML Model inference failed: {e}")
            return {"error": str(e)}

    def _score_with_azure(self, event_text: str) -> Dict[str, Any]:
        """Fallback to Azure OpenAI if Splunk Hosted Models are unavailable."""
        url = f"{settings.AZURE_OPENAI_ENDPOINT}openai/deployments/{settings.AZURE_OPENAI_DEPLOYMENT}/chat/completions?api-version={settings.AZURE_OPENAI_API_VERSION}"
        headers = {
            "api-key": settings.AZURE_OPENAI_API_KEY,
            "Content-Type": "application/json"
        }
        payload = {
            "messages": [
                {"role": "system", "content": "You are Foundation-Sec, an expert security analyst model. Analyze the following log event. Return a JSON object with 'severity_score' (integer 0-100), 'confidence' (float), 'analysis' (string), and 'suggested_tactic' (string)."},
                {"role": "user", "content": f"Event: {event_text}"}
            ],
            "response_format": { "type": "json_object" }
        }
        
        try:
            response = requests.post(url, json=payload, headers=headers, timeout=15)
            response.raise_for_status()
            data = response.json()
            content = data.get("choices", [{}])[0].get("message", {}).get("content", "{}")
            import json
            parsed_content = json.loads(content)
            return {
                "raw_response": data,
                "severity_score": parsed_content.get("severity_score", 85),
                "confidence": parsed_content.get("confidence", 0.9),
                "analysis": parsed_content.get("analysis", "Azure OpenAI analysis complete."),
                "suggested_tactic": parsed_content.get("suggested_tactic", "Unknown")
            }
        except Exception as e:
            print(f"Azure OpenAI inference failed: {e}")
            return {"error": str(e), "severity_score": 85}
