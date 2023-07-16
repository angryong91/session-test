from uuid import uuid4

import bcrypt
from fastapi import APIRouter, Depends, Response

from app.common.consts import SETTINGS
from app.database.schema import Users
from app.exceptions import BadRequest, NotFoundUser, DeletedUser, BlockedUser, InactiveUser, InvalidToken
from app.models import MessageOk, UserStatus, VerificationUrl, TokenType, \
    SessionInfo, SignupPayload, TokenQueryParam, SigninPayload
from app.utils.session import backend, cookie
from app.utils.token import token_decode, create_token

router = APIRouter(prefix="/auth")


@router.post("/signup", status_code=201, response_model=VerificationUrl)
async def sign_up(payload: SignupPayload):
    """
        `sign up api`\n
        :param auth_info:
        :return:
    """
    user = Users.get(email=payload.email)
    if user:
        raise BadRequest(msg="Exist User")

    password = bcrypt.hashpw(payload.password.encode("utf-8"), bcrypt.gensalt())
    new_user = Users.create(auto_commit=True,  email=payload.email, password=password,
                            first_name=payload.first_name, last_name=payload.last_name,
                            privacy_n_policy_accept=payload.privacy_n_policy_accept)
    data = {"id": new_user.id, "email": new_user.email, "type": TokenType.verify}
    verification_token = create_token(data)
    # Todo: send to user verification email

    url = f"http://{SETTINGS.DOMAIN}:{SETTINGS.PORT}/v1/auth/verify?token={verification_token}"
    return VerificationUrl(verification_url=url)


@router.get("/verify", status_code=200, response_model=MessageOk)
def verify_email(query_param: TokenQueryParam = Depends()):
    """
        `verify email api `\n
        :param query_param:
        :return:
    """
    payload = token_decode(query_param.token)
    if payload.get("type") != TokenType.verify:
        raise InvalidToken()

    user_filter = Users.filter(id=payload.get("id"))

    if not user_filter.first():
        raise NotFoundUser()

    user_filter.update(auto_commit=True, status=UserStatus.active)

    return MessageOk()


@router.post("/signin", status_code=200, response_model=MessageOk)
async def sign_in(payload: SigninPayload, response: Response):
    """
        `sign in api`\n
        :param response:
        :param payload:
        :return:
    """
    user = Users.get(email=payload.email)
    if not user:
        raise NotFoundUser()

    if user.status == UserStatus.inactive:
        raise InactiveUser()
    elif user.status == UserStatus.deleted:
        raise DeletedUser()
    elif user.status == UserStatus.blocked:
        raise BlockedUser()

    is_verified = bcrypt.checkpw(payload.password.encode("utf-8"), user.password)
    if not is_verified:
        raise BadRequest(msg="Invalid Password")

    session = uuid4()
    data = SessionInfo(user_id=user.id)

    # register session in memory
    await backend.create(session, data)
    # set cookie in response
    cookie.attach_to_response(response, session)

    return MessageOk()
