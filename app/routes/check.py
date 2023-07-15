from datetime import datetime

from fastapi import APIRouter
from starlette.responses import Response

# from app.routes import rate_limiter

router = APIRouter()


@router.get("/check")
async def check():
    """
    health check api
    :return:
    """
    current_time = datetime.utcnow()
    return Response(f"UTC: {current_time.strftime('%Y.%m.%d %H:%M:%S')}")
