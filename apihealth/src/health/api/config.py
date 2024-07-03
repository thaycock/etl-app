import logging
from typing import Optional

from flask import request


class FlaskAppConfig:
    """Basic flask app configuration"""


def get_username() -> Optional[str]:
    return request.headers.get("username")


def get_uuid(request) -> Optional[str]:
    logging.error(request)
    return request.headers.get("uuid")
