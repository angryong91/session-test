from enum import Enum
from typing import Optional

from fastapi import Query
from humps import camel
from pydantic import Field
from pydantic.main import BaseModel


class SnsType(str, Enum):
    email: str = "email"
    google: str = "google"
    kakao: str = "kakao"


class TokenType(str, Enum):
    verify: str = "verify"
    access: str = "access"
    refresh: str = "refresh"


class UserStatus(str, Enum):
    inactive: str = "inactive"
    active: str = "active"
    blocked: str = "blocked"
    deleted: str = "deleted"


def to_camel(string):
    return camel.case(string)


class CamelModel(BaseModel):
    class Config:
        alias_generator = to_camel
        allow_population_by_field_name = True


class MessageOk(CamelModel):
    msg: str = Field(default="OK")


class VerificationUrl(CamelModel):
    verification_url: str = Field(None, example="http://localhost:8080/verify?token={verification_token}")


class QueryParamToken(CamelModel):
    token: str = Query(None, example="{verification_token}")


class Token(CamelModel):
    access_token: str = Field(None, example="{access_token for 30 days}")
    refresh_token: str = Field(None, example="{refresh_token for 60 days}")


class UserEmail(CamelModel):
    email: Optional[str] = Field(None, example="91angryong@gmail.com", nullable=True)


class AuthRequest(UserEmail):
    password: str = Field(example="{user_password}")


class UserInfo(CamelModel):
    id: str = Field(example="{uuid}")
    email: str = Field(None, example="91angryong@gmail.com")
    sns_type: SnsType = Field(None, example=SnsType.email)
    status: UserStatus = Field(None, example=UserStatus.active)

    class Config:
        orm_mode = True
