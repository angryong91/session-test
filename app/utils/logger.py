import json
import logging
import os
import traceback
from datetime import timedelta, datetime
from logging.handlers import RotatingFileHandler
from time import time

from fastapi.logger import logger
from fastapi.requests import Request

from app.common.consts import SETTINGS

log_file_path = os.path.join(SETTINGS.BASE_DIR, "logs/server.log")
if not os.path.exists(os.path.dirname(log_file_path)):
    os.makedirs(os.path.dirname(log_file_path))

file_handler = RotatingFileHandler(log_file_path, maxBytes=1024 * 1024 * 100, backupCount=5)
stream_handler = logging.StreamHandler()

logger.addHandler(file_handler)
logger.addHandler(stream_handler)
logger.setLevel(logging.DEBUG)


async def api_logger(request: Request, response=None, error=None):
    time_format = "%Y/%m/%d %H:%M:%S"
    t = time() - request.state.start
    status_code = error.status_code if error else response.status_code
    error_log = None
    user = request.state.user
    hostname = SETTINGS.DOMAIN
    path = request.url.path if request.url.path else ""
    query_params = dict(request.query_params)

    if error:
        msg = error.msg if status_code in [400, 401, 403] else error.ex
        error_log = dict(
            raised=str(error.__class__.__name__),
            msg=str(msg),
            detail=str(error.detail)
        )

    user_log = dict(
        client=request.state.ip,
        user=user.id if user and user.id else None,
        email=user.email if user and user.email else None,
    )

    log_dict = dict(
        url=str(hostname + path),
        method=str(request.method),
        statusCode=status_code,
        query_params=str(query_params),
        errorDetail=str(error_log),
        client=str(user_log),
        processedTime=str(round(t * 1000, 5)) + "ms",
        datetimeUTC=datetime.utcnow().strftime(time_format),
        datetimeKST=(datetime.utcnow() + timedelta(hours=9)).strftime(time_format),
    )
    if error and error.status_code >= 500:
        logger.error(traceback.format_exc())
        logger.error(json.dumps(log_dict))
    else:
        logger.info(json.dumps(log_dict))
