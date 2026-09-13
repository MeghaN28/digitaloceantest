from dataclasses import dataclass


@dataclass
class AppQuotaPlan:
    app_id: str
    plan_id: str
