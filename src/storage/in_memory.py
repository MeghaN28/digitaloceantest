from datetime import datetime
from typing import Dict, List, Optional

from src.core.config import settings
from src.domain.event import DomainEvent


class InMemoryEventStore:
    _PLAN_ALIASES = {
        "starter": "basic",
        "basic": "basic",
        "pro": "pro",
        "premium": "pro",
    }

    def __init__(self):
        self._events: List[DomainEvent] = []
        self._dedupe: Dict[str, str] = {}
        self._app_plans: Dict[str, str] = {}
        self._plans: Dict[str, Dict[str, int]] = {
            "basic": {"rps": settings.BASIC_RPS},
            "pro": {"rps": settings.PRO_RPS},
        }

    @classmethod
    def normalize_plan_id(cls, plan_id: Optional[str]) -> str:
        if not plan_id:
            return "basic"
        return cls._PLAN_ALIASES.get(plan_id.lower(), "basic")

    async def append_event(self, event: DomainEvent) -> str:
        if event.client_event_id:
            key = f"{event.app_id}:{event.client_event_id}"
            if key in self._dedupe:
                return self._dedupe[key]
            self._dedupe[key] = event.id
        self._events.append(event)
        if event.plan_id:
            self._app_plans[event.app_id] = self.normalize_plan_id(event.plan_id)
        return event.id

    async def set_app_plan(self, app_id: str, plan_id: str) -> str:
        normalized = self.normalize_plan_id(plan_id)
        self._app_plans[app_id] = normalized
        return normalized

    async def get_app_plan(self, app_id: str) -> str:
        return self._app_plans.get(app_id, "basic")

    async def get_plan_details(self, plan_id: str) -> Dict[str, int]:
        normalized = self.normalize_plan_id(plan_id)
        return {"rps": self._plans[normalized]["rps"]}

    async def list_plans(self) -> Dict[str, Dict[str, int]]:
        return {
            name: {"rps": plan_data["rps"]}
            for name, plan_data in self._plans.items()
        }

    async def list_events_by_app(self, app_id: str) -> List[DomainEvent]:
        return [e for e in self._events if e.app_id == app_id]

    async def get_event_by_id(self, event_id: str) -> Optional[DomainEvent]:
        for e in self._events:
            if e.id == event_id:
                return e
        return None

    async def list_events_by_app_and_window(self, app_id: str, start: datetime, end: datetime) -> List[DomainEvent]:
        return [e for e in self._events if e.app_id == app_id and start <= e.timestamp <= end]
