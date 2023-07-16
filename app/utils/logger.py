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
    hostname = SETTINGS.DOMAIN
    path = request.url.path if request.url.path else ""

    if error:
        error_log = dict(
            raised=str(error.__class__.__name__),
            msg=str(error.msg),
            detail=str(error.detail)
        )

    log_dict = dict(
        url=str(hostname + path),
        method=str(request.method),
        statusCode=status_code,
        errorDetail=str(error_log),
        client=str(request.state.ip),
        processedTime=str(round(t * 1000, 5)) + "ms",
        datetimeUTC=datetime.utcnow().strftime(time_format),
        datetimeKST=(datetime.utcnow() + timedelta(hours=9)).strftime(time_format),
    )
    if error and error.status_code >= 500:
        logger.error(traceback.format_exc())
        logger.error(json.dumps(log_dict))
    else:
        logger.info(json.dumps(log_dict))
