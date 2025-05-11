# storm/common/decorators/http/redirect.py

from typing import Callable, Optional

from storm.common.constants import REDIRECT_METADATA
from storm.core.di.reflect import Reflect


class Redirect:
    """
    Decorator that marks a route to redirect to a given URL.

    :param url: The URL to redirect to.
    :param status_code: Optional HTTP status code (e.g., 302).
    """

    def __init__(self, url: str = "", status_code: Optional[int] = None):
        self.url = url
        self.status_code = status_code

    def __call__(self, func: Callable) -> Callable:
        Reflect.define_metadata(REDIRECT_METADATA, {"url": self.url, "statusCode": self.status_code}, func)
        return func
