from fastapi import FastAPI, Request

from src.core.config import Settings
from src.core.errors import DomainError, http_exception_handler
from src.api.v1.routes.events import router as events_router
from src.api.v1.routes.health import router as health_router
from src.api.v1.routes.quota import router as quota_router
from src.storage.in_memory import InMemoryEventStore

settings = Settings()

app = FastAPI(title="Usage API")

# simple in-memory store instance; replaceable via config
app.state.event_store = InMemoryEventStore()

app.include_router(events_router, prefix="/api/v1")
app.include_router(quota_router, prefix="/api/v1")
app.include_router(health_router)

@app.exception_handler(DomainError)
async def _domain_exc_handler(request: Request, exc: DomainError):
    return await http_exception_handler(request, exc)

@app.get("/")
async def root():
    return {"service": "usage-api", "env": settings.ENV}
