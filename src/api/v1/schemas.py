from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime

class EventCreate(BaseModel):
    app_id: str
    plan_id: str
    no_of_req: int = Field(..., gt=0)
    quota: str
    resource_type: Optional[str] = "requests"
    client_event_id: Optional[str] = None
    version: Optional[int] = 1

class EventResponse(BaseModel):
    event_id: str

class UsageResponse(BaseModel):
    app_id: str
    usage_month_total: int
    usage_month_to_date: int
    quota_plan: str
    quota_rps: int
    quota_month_total: int
    quota_month_to_date: int
