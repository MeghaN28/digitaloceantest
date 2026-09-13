from abc import ABC, abstractmethod
from typing import List, Optional

from src.domain.event import DomainEvent


class EventStore(ABC):
    @abstractmethod
    async def append_event(self, event: DomainEvent) -> str:
        raise NotImplementedError()

    @abstractmethod
    async def list_events_by_app(self, app_id: str) -> List[DomainEvent]:
        raise NotImplementedError()

    @abstractmethod
    async def get_event_by_id(self, event_id: str) -> Optional[DomainEvent]:
        raise NotImplementedError()
