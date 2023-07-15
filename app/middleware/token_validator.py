import time
from typing import Callable, Awaitable

from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import JSONResponse, StreamingResponse

from app.database.schema import Users
from app.exceptions import exception_handler, NotFoundUser, DeletedUser, BlockedUser, InvalidToken
from app.models import UserStatus, TokenType
from app.utils.logger import api_logger
from app.utils.token import token_decode


class TokenValidMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next: Callable[[Request], Awaitable[StreamingResponse]]):
        request.state.start = time.time()
        request.state.user = None
        ip = request.headers["x-forwarded-for"] if "x-forwarded-for" in request.headers.keys() else request.client.host
        request.state.ip = ip.split(",")[0] if "," in ip else ip
        headers = request.headers
        try:
            check_authorization(request, headers)
            response = await call_next(request)
            await api_logger(request=request, response=response)
        except Exception as e:
            error = exception_handler(e)
            error_dict = dict(status=error.status_code, msg=error.msg, detail=error.detail, code=error.code)
            response = JSONResponse(status_code=error.status_code, content=error_dict)
            await api_logger(request=request, error=error)

        return response


def check_authorization(request, headers):
    if "authorization" in headers.keys():
        payload = token_decode(headers.get("authorization"))
        if payload.get("type") != TokenType.access:
            raise InvalidToken()

        user = Users.get(id=payload.get("id"))
        if not user:
            raise NotFoundUser()
        if user.status == UserStatus.deleted:
            raise DeletedUser()
        elif user.status == UserStatus.blocked:
            raise BlockedUser()

        request.state.user = user
