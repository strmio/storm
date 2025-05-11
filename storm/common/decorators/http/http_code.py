# storm/common/decorators/http/http_code.py

from typing import Callable

from storm.common.constants import HTTP_CODE_METADATA
from storm.core.di.reflect import Reflect


class HttpCode:
    """
    Decorator that sets the HTTP status code for the response.

    :param status_code: The HTTP status code to return (e.g., 200, 404, 201).
    """

    def __init__(self, status_code: int):
        self.status_code = status_code

    def __call__(self, func: Callable) -> Callable:
        Reflect.define_metadata(HTTP_CODE_METADATA, self.status_code, func)
        return func
