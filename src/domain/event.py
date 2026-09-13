from dataclasses import dataclass
from datetime import datetime, timezone
from typing import Optional
import uuid


@dataclass
class DomainEvent:
    id: str
    app_id: str
    plan_id: str
    no_of_req: int
    quota: str
    resource_type: str
    timestamp: datetime
    version: int = 1
    client_event_id: Optional[str] = None

    @staticmethod
    def new(app_id: str, plan_id: str, no_of_req: int, quota: str, resource_type: str = "requests", client_event_id: Optional[str] = None, version: int = 1):
        return DomainEvent(
            id=str(uuid.uuid4()),
            app_id=app_id,
            plan_id=plan_id,
            no_of_req=no_of_req,
            quota=quota,
            resource_type=resource_type,
            timestamp=datetime.now(timezone.utc),
            version=version,
            client_event_id=client_event_id,
        )
