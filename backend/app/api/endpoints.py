from fastapi import APIRouter, Request, BackgroundTasks
from pydantic import BaseModel
from typing import Dict, Any
from app.tasks import process_splunk_alert

router = APIRouter()

class AlertPayload(BaseModel):
    result: Dict[str, Any]
    search_name: str = "Unknown Search"
    sid: str = ""
    app: str = "search"

@router.post("/webhook/splunk")
async def splunk_webhook(alert: AlertPayload, request: Request, background_tasks: BackgroundTasks):
    """
    Endpoint to receive alerts from Splunk via Webhook.
    """
    # We dispatch the alert to FastAPI's built-in background tasks queue
    background_tasks.add_task(process_splunk_alert, alert.model_dump())
    
    return {
        "status": "accepted",
        "message": "Alert received and dispatched for background processing"
    }

import redis
import json
from app.core.config import settings

redis_client = redis.from_url(settings.REDIS_URL)

@router.get("/alerts")
async def get_alerts():
    """
    Endpoint to fetch the latest incident reports for the dashboard.
    """
    raw_alerts = redis_client.lrange("recent_alerts", 0, -1)
    alerts = [json.loads(a) for a in raw_alerts]
    return alerts
