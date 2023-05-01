from starlette.exceptions import HTTPException
from starlette.requests import Request
from starlette.responses import JSONResponse


async def http_exception(request: Request, exc: HTTPException):
    return JSONResponse({"detail": exc.detail}, status_code=exc.status_code)


async def handle_error(request: Request, exc: Exception):
    return JSONResponse({"detail": exc.detail}, status_code=exc.status_code)


exception_handlers = {
    HTTPException: http_exception,
    Exception: handle_error
}
