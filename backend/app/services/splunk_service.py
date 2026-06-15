import splunklib.client as client
import splunklib.results as results
from app.core.config import settings

class SplunkService:
    def __init__(self):
        self.host = settings.SPLUNK_HOST.replace("https://", "").replace("http://", "")
        self.port = settings.SPLUNK_PORT
        self.username = settings.SPLUNK_USERNAME
        self.password = settings.SPLUNK_PASSWORD
        self.token = settings.SPLUNK_TOKEN
        self.service = self._connect()

    def _connect(self):
        try:
            import socket
            socket.setdefaulttimeout(15)
            if self.token:
                return client.connect(
                    host=self.host,
                    port=self.port,
                    token=self.token,
                    autologin=True,
                    verify=settings.SPLUNK_VERIFY_TLS
                )
            elif self.username and self.password:
                return client.connect(
                    host=self.host,
                    port=self.port,
                    username=self.username,
                    password=self.password,
                    autologin=True,
                    verify=settings.SPLUNK_VERIFY_TLS
                )
            else:
                return None # Used for mocking if no credentials are set yet
        except Exception as e:
            print(f"Error connecting to Splunk: {e}")
            return None

    def execute_search(self, query: str) -> list:
        if not self.service:
            print("Error: Splunk service not connected. Cannot execute search.")
            return []
            
        kwargs_oneshot = {"earliest_time": "-24h", "latest_time": "now"}
        search_query = query if query.startswith("search") else f"search {query}"
        
        try:
            oneshot_search_results = self.service.jobs.oneshot(search_query, **kwargs_oneshot)
            reader = results.ResultsReader(oneshot_search_results)
            events = []
            for item in reader:
                if isinstance(item, dict):
                    events.append(item)
            return events
        except Exception as e:
            print(f"Search execution failed: {e}")
            return []
