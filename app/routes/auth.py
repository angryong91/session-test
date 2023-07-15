import bcrypt
from fastapi import APIRouter, Depends

from app.common.consts import SETTINGS
from app.database.schema import Users
from app.exceptions import BadRequest, NotFoundUser, DeletedUser, BlockedUser, InactiveUser, InvalidToken
from app.models import AuthRequest, Token, UserInfo, MessageOk, UserStatus, VerificationUrl, QueryParamToken, TokenType
from app.utils.token import get_tokens, token_decode, create_token

router = APIRouter(prefix="/auth")


@router.post("/signup", status_code=201, response_model=VerificationUrl)
async def sign_up(auth_info: AuthRequest):
    """
        `sign up api`\n
        :param auth_info:
        :return:
    """
    user = Users.get(email=auth_info.email)
    if user:
        raise BadRequest(msg="Exist User")

    # Todo: Password validation

    password = bcrypt.hashpw(auth_info.password.encode("utf-8"), bcrypt.gensalt())
    new_user = Users.create(auto_commit=True, password=password, email=auth_info.email)
    data = {"id": new_user.id, "email": new_user.email, "type": TokenType.verify}
    verification_token = create_token(data)
    # Todo: send to user verification email

    return VerificationUrl(verification_url=f"http://{SETTINGS.DOMAIN}:{SETTINGS.PORT}/v1/auth/verify?token={verification_token}")


@router.get("/verify", status_code=200, response_model=MessageOk)
def verify_email(query_param: QueryParamToken = Depends()):
    payload = token_decode(query_param.token)
    if payload.get("type") != TokenType.verify:
        raise InvalidToken()

    user_filter = Users.filter(id=payload.get("id"))

    if not user_filter.first():
        raise NotFoundUser()

    user_filter.update(auto_commit=True, status=UserStatus.active)

    return MessageOk()


@router.post("/signin", status_code=200, response_model=Token)
async def sign_in(auth_info: AuthRequest):
    """
        `sign in api`\n
        :param auth_info:
        :return:
    """
    user = Users.get(email=auth_info.email)
    if not user:
        raise NotFoundUser()

    if user.status == UserStatus.inactive:
        raise InactiveUser()
    elif user.status == UserStatus.deleted:
        raise DeletedUser()
    elif user.status == UserStatus.blocked:
        raise BlockedUser()

    is_verified = bcrypt.checkpw(auth_info.password.encode("utf-8"), user.password)
    if not is_verified:
        raise BadRequest(msg="Invalid Password")

    return get_tokens(user)


@router.post("/refresh", status_code=200, response_model=Token)
async def check_refresh(refresh_token: str):
    """
    :param refresh_token:
    :return:
    """
    payload = token_decode(refresh_token)
    if payload.get("type") != TokenType.refresh:
        raise InvalidToken()

    user_info = UserInfo(**payload)
    user = Users.get(id=user_info.id, email=user_info.email, status=UserStatus.active)
    if user:
        return get_tokens(user)
    else:
        raise NotFoundUser()
