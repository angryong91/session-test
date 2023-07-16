from uuid import UUID

from fastapi_sessions.backends.implementations import InMemoryBackend
from fastapi_sessions.frontends.implementations import SessionCookie, CookieParameters
from fastapi_sessions.session_verifier import SessionVerifier

from app.common.consts import SETTINGS
from app.exceptions import InvalidSession
from app.models import SessionInfo


class BasicVerifier(SessionVerifier[UUID, SessionInfo]):
    def __init__(self, backend: InMemoryBackend[UUID, SessionInfo]):
        self._identifier = SETTINGS.SESSION_IDENTIFIER_NAME
        self._auto_error = True
        self._backend = backend
        self._auth_http_exception = InvalidSession()

    @property
    def identifier(self):
        return self._identifier

    @property
    def backend(self):
        return self._backend

    @property
    def auto_error(self):
        return self._auto_error

    @property
    def auth_http_exception(self):
        return self._auth_http_exception

    def verify_session(self, model: SessionInfo) -> bool:
        """If the session exists, it is valid"""
        return True


cookie_params = CookieParameters()
cookie = SessionCookie(
        cookie_name=SETTINGS.SESSION_COOKIE_NAME,
        identifier=SETTINGS.SESSION_IDENTIFIER_NAME,
        auto_error=True,
        secret_key=SETTINGS.SESSION_SECRET_KEY,
        cookie_params=cookie_params,
    )
backend = InMemoryBackend[UUID, SessionInfo]()
verifier = BasicVerifier(backend)
