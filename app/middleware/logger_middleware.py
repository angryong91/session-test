import time
from typing import Callable, Awaitable

from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import JSONResponse, StreamingResponse
from app.exceptions import exception_handler
from app.utils.logger import api_logger


class LoggerMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next: Callable[[Request], Awaitable[StreamingResponse]]):
        request.state.start = time.time()
        request.state.service = None
        ip = request.headers["x-forwarded-for"] if "x-forwarded-for" in request.headers.keys() else request.client.host
        request.state.ip = ip.split(",")[0] if "," in ip else ip
        try:
            response = await call_next(request)
            await api_logger(request=request, response=response)
        except Exception as e:
            error = exception_handler(e)
            error_dict = dict(status=error.status_code, msg=error.msg, detail=error.detail, code=error.code)
            response = JSONResponse(status_code=error.status_code, content=error_dict)
            await api_logger(request=request, error=error)

        return response
