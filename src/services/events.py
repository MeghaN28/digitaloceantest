from datetime import datetime, timezone
from typing import Optional

from src.api.v1.schemas import EventCreate, UsageResponse
from src.core.config import settings
from src.core.errors import BadRequestError
from src.domain.event import DomainEvent
from src.storage.in_memory import InMemoryEventStore


async def resolve_plan_for_app(app_id: str, store: InMemoryEventStore) -> str:
    return await store.get_app_plan(app_id)


async def submit_event(event_in: EventCreate, store: InMemoryEventStore) -> str:
    if event_in.no_of_req <= 0:
        raise BadRequestError("no_of_req must be > 0")

    plan_id = store.normalize_plan_id(event_in.plan_id or event_in.quota)
    await store.set_app_plan(event_in.app_id, plan_id)

    domain_event = DomainEvent.new(
        app_id=event_in.app_id,
        plan_id=plan_id,
        no_of_req=event_in.no_of_req,
        quota=plan_id,
        resource_type=event_in.resource_type,
        client_event_id=event_in.client_event_id,
        version=event_in.version or 1,
    )

    return await store.append_event(domain_event)


async def compute_usage(app_id: str, store: InMemoryEventStore, now: Optional[datetime] = None) -> UsageResponse:
    now = now or datetime.now(timezone.utc)
    month_start = datetime(now.year, now.month, 1, tzinfo=timezone.utc)
    if now.month == 12:
        next_month = datetime(now.year + 1, 1, 1, tzinfo=timezone.utc)
    else:
        next_month = datetime(now.year, now.month + 1, 1, tzinfo=timezone.utc)

    events_month = await store.list_events_by_app_and_window(app_id, month_start, next_month)
    total_month = sum(e.no_of_req for e in events_month)
    total_mtd = sum(e.no_of_req for e in events_month if e.timestamp <= now)

    plan = await resolve_plan_for_app(app_id, store)

    seconds_in_month = int((next_month - month_start).total_seconds())
    seconds_mtd = int((now - month_start).total_seconds()) + 1

    if plan == "pro":
        rps = settings.PRO_RPS
    else:
        rps = settings.BASIC_RPS

    quota_month = rps * seconds_in_month
    quota_mtd = rps * seconds_mtd

    return UsageResponse(
        app_id=app_id,
        usage_month_total=total_month,
        usage_month_to_date=total_mtd,
        quota_plan=plan,
        quota_rps=rps,
        quota_month_total=quota_month,
        quota_month_to_date=quota_mtd,
    )
