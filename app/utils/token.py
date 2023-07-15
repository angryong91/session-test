from datetime import timedelta, datetime

import jwt
from jwt import ExpiredSignatureError, InvalidTokenError

from app.common.consts import SETTINGS
from app.exceptions import ExpiredToken, InvalidToken
from app.models import TokenType


def get_tokens(user):
    access_token_expires = timedelta(days=SETTINGS.JWT_ACCESS_TOKEN_EXPIRE_DAY)
    refresh_token_expires = timedelta(days=SETTINGS.JWT_REFRESH_TOKEN_EXPIRE_DAY)
    return dict(
        access_token=create_token(data={"id": user.id, "email": user.email, "type": TokenType.access},
                                  expired_delta=access_token_expires),
        refresh_token=create_token(data={"id": user.id, "email": user.email, "type": TokenType.refresh},
                                   expired_delta=refresh_token_expires)
    )


def create_token(data: dict = None, expired_delta: timedelta = None):
    if expired_delta:
        expired_date = datetime.utcnow() + expired_delta
    else:
        expired_date = datetime.utcnow() + timedelta(minutes=15)
    data.update({"exp": expired_date})
    encoded_jwt = jwt.encode(data, SETTINGS.JWT_SECRET_KEY, algorithm=SETTINGS.JWT_ALGORITHM)
    return encoded_jwt


def token_decode(jwt_token):
    try:
        return jwt.decode(jwt_token.replace("Bearer ", ""), key=SETTINGS.JWT_SECRET_KEY,
                          algorithms=[SETTINGS.JWT_ALGORITHM])
    except ExpiredSignatureError:
        raise ExpiredToken()
    except InvalidTokenError:
        raise InvalidToken()
