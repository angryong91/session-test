def exception_handler(error: Exception):
    if not isinstance(error, APIException):
        error = APIException(ex=error, detail=str(error))
    return error


class StatusCode:
    HTTP_500 = 500
    HTTP_400 = 400
    HTTP_401 = 401
    HTTP_403 = 403
    HTTP_404 = 404
    HTTP_409 = 409


class APIException(Exception):
    status_code: int
    code: str
    msg: str
    detail: str
    ex: Exception

    def __init__(self, status_code: int = StatusCode.HTTP_500, code: str = "000000", msg: str = None,
                 detail: str = None, ex: Exception = None):
        self.status_code = status_code
        self.code = code
        self.msg = msg
        self.detail = detail
        self.ex = ex
        super().__init__(ex)


class BadRequest(APIException):
    def __init__(self, msg: str = "Bad Request", ex: Exception = None):
        super().__init__(
            status_code=StatusCode.HTTP_400,
            msg=msg,
            code=f"{StatusCode.HTTP_400}{'1'.zfill(4)}",
            ex=ex,
        )


class NotFoundUser(APIException):
    def __init__(self, ex: Exception = None):
        super().__init__(
            status_code=StatusCode.HTTP_400,
            msg="Not Found User",
            code=f"{StatusCode.HTTP_400}{'2'.zfill(4)}",
            ex=ex,
        )


class UnAuthorized(APIException):
    def __init__(self, ex: Exception = None):
        super().__init__(
            status_code=StatusCode.HTTP_401,
            msg="Authorization Required",
            code=f"{StatusCode.HTTP_401}{'1'.zfill(4)}",
            ex=ex,
        )


class ExpiredToken(APIException):
    def __init__(self, ex: Exception = None):
        super().__init__(
            status_code=StatusCode.HTTP_401,
            msg="Expired Token",
            code=f"{StatusCode.HTTP_401}{'2'.zfill(4)}",
            ex=ex,
        )


class InvalidToken(APIException):
    def __init__(self, ex: Exception = None):
        super().__init__(
            status_code=StatusCode.HTTP_401,
            msg="Invalid Token",
            code=f"{StatusCode.HTTP_401}{'3'.zfill(4)}",
            ex=ex,
        )


class NotAllowed(APIException):
    def __init__(self, msg: str = "Not Allowed", ex: Exception = None):
        super().__init__(
            status_code=StatusCode.HTTP_403,
            msg=msg,
            code=f"{StatusCode.HTTP_403}{'1'.zfill(4)}",
            ex=ex,
        )


class InactiveUser(APIException):
    def __init__(self, ex: Exception = None):
        super().__init__(
            status_code=StatusCode.HTTP_403,
            msg="Inactive User",
            code=f"{StatusCode.HTTP_403}{'2'.zfill(4)}",
            ex=ex,
        )


class DeletedUser(APIException):
    def __init__(self, ex: Exception = None):
        super().__init__(
            status_code=StatusCode.HTTP_403,
            msg="Deleted User",
            code=f"{StatusCode.HTTP_403}{'3'.zfill(4)}",
            ex=ex,
        )


class BlockedUser(APIException):
    def __init__(self, ex: Exception = None):
        super().__init__(
            status_code=StatusCode.HTTP_403,
            msg="Blocked User",
            code=f"{StatusCode.HTTP_403}{'4'.zfill(4)}",
            ex=ex,
        )
