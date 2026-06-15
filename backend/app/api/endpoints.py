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
async def splunk_webhook(alert: AlertPayload, request: Request):
    """
    Endpoint to receive alerts from Splunk via Webhook.
    """
    # In a real scenario, you'd validate the request token/signature here
    
    # We dispatch the alert to our Celery task queue for asynchronous processing
    task = process_splunk_alert.delay(alert.model_dump())
    
    return {
        "status": "accepted",
        "message": "Alert received and dispatched for processing",
        "task_id": task.id
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
