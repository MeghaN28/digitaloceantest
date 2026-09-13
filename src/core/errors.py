from fastapi import Request
from fastapi.responses import JSONResponse

class DomainError(Exception):
    status_code = 500
    def __init__(self, detail: str = "" ):
        self.detail = detail
        super().__init__(detail)

class NotFoundError(DomainError):
    status_code = 404

class ConflictError(DomainError):
    status_code = 409

class BadRequestError(DomainError):
    status_code = 400

async def http_exception_handler(request: Request, exc: DomainError):
    return JSONResponse(status_code=getattr(exc, "status_code", 500), content={"error": exc.detail})
