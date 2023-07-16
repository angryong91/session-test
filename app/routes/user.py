from fastapi import APIRouter, Depends

from app.database.schema import Users
from app.exceptions import NotFoundUser, DeletedUser, BlockedUser, InactiveUser
from app.models import UserInfo, UserStatus, SessionInfo
from app.utils.session import verifier, cookie

router = APIRouter(prefix="/user")


@router.get("", status_code=200, response_model=UserInfo, dependencies=[Depends(cookie)])
async def get_user_info(session_info: SessionInfo = Depends(verifier)):
    """
    :param session_info:
    :return:
    """
    user = Users.get(id=session_info.user_id)
    if not user:
        raise NotFoundUser()

    if user.status == UserStatus.inactive:
        raise InactiveUser()
    elif user.status == UserStatus.deleted:
        raise DeletedUser()
    elif user.status == UserStatus.blocked:
        raise BlockedUser()

    return user
