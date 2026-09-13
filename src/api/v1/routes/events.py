from fastapi import APIRouter, HTTPException, Request

from src.api.v1.schemas import EventCreate, EventResponse, UsageResponse
from src.core.errors import BadRequestError
from src.services.events import compute_usage, submit_event
from src.storage.in_memory import InMemoryEventStore

router = APIRouter()


@router.post("/events", response_model=EventResponse, status_code=201)
@router.post("/usage", response_model=EventResponse, status_code=201)
async def create_event(event: EventCreate, request: Request):
    store: InMemoryEventStore = request.app.state.event_store
    try:
        event_id = await submit_event(event, store)
    except BadRequestError as exc:
        raise HTTPException(status_code=exc.status_code, detail=exc.detail) from exc
    return EventResponse(event_id=event_id)


@router.get("/usage", response_model=UsageResponse)
async def get_usage_query(app_id: str | None = None, request: Request = None):
    if app_id is None:
        raise HTTPException(status_code=400, detail="Missing required query parameter: app_id")
    store: InMemoryEventStore = request.app.state.event_store
    usage = await compute_usage(app_id, store)
    return usage


@router.get("/apps/{app_id}/usage", response_model=UsageResponse)
async def get_usage_path(app_id: str, request: Request):
    store: InMemoryEventStore = request.app.state.event_store
    usage = await compute_usage(app_id, store)
    return usage
