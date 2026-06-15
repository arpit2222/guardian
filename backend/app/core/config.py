from pydantic_settings import BaseSettings
from typing import List

class Settings(BaseSettings):
    PROJECT_NAME: str = "SENTINEL_API"
    API_V1_STR: str = "/api/v1"
    CORS_ORIGINS: List[str] = ["http://localhost:3000"]
    
    # Celery & Redis
    REDIS_URL: str = "redis://localhost:6379/0"
    
    # Splunk
    SPLUNK_HOST: str = "https://your-splunk-instance.splunkcloud.com"
    SPLUNK_PORT: int = 8089
    SPLUNK_USERNAME: str = ""
    SPLUNK_PASSWORD: str = ""
    SPLUNK_TOKEN: str = ""
    SPLUNK_VERIFY_TLS: bool = True
    
    # ML Models (Splunk)
    SPLUNK_ML_ENDPOINT: str = ""
    SPLUNK_ML_TOKEN: str = ""
    
    # ML Models (Azure OpenAI Fallback)
    AZURE_OPENAI_API_KEY: str = ""
    AZURE_OPENAI_ENDPOINT: str = ""
    AZURE_OPENAI_DEPLOYMENT: str = "gpt-5.4"
    AZURE_OPENAI_API_VERSION: str = "2024-02-15-preview"
    
    # Threat Intel
    VIRUSTOTAL_API_KEY: str = ""
    ALIENVAULT_API_KEY: str = ""
    
    # Notifications
    DISCORD_WEBHOOK_URL: str = ""

    class Config:
        env_file = ".env"
        case_sensitive = True

settings = Settings()
