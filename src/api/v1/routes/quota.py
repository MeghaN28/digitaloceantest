from fastapi import APIRouter, Request

from src.core.config import settings
from src.storage.in_memory import InMemoryEventStore

router = APIRouter()


@router.get("/quota-plan")
@router.get("/plans")
async def quota_plan(request: Request = None):
    if request is not None and hasattr(request.app.state, "event_store"):
        store: InMemoryEventStore = request.app.state.event_store
        return await store.list_plans()
    return {
        "basic": {"rps": settings.BASIC_RPS},
        "pro": {"rps": settings.PRO_RPS},
    }


@router.get("/apps/{app_id}/plan")
async def app_plan(app_id: str, request: Request):
    store: InMemoryEventStore = request.app.state.event_store
    plan_id = await store.get_app_plan(app_id)
    plan_details = await store.get_plan_details(plan_id)
    return {"app_id": app_id, "plan": plan_id, "rps": plan_details["rps"]}
