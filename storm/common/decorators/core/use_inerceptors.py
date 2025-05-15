from typing import Any, Callable, Optional, Type, Union

from storm.common.constants import INTERCEPTORS_METADATA
from storm.common.utils.extend_metadata import extend_array_metadata
from storm.common.utils.shared import is_function
from storm.common.utils.validate_each import validate_each


def is_interceptor_valid(interceptor: Any) -> bool:
    """
    Validates whether the given object is a valid interceptor.

    A valid interceptor is either a class with an `intercept` method
    or an instance with a callable `intercept` method.

    :param interceptor: The object to validate.
    :return: True if valid, False otherwise.
    """
    if not interceptor:
        return False

    if is_function(interceptor):
        return hasattr(interceptor, "intercept") or hasattr(interceptor(), "intercept")

    return hasattr(interceptor, "intercept") and callable(getattr(interceptor, "intercept", None))


class UseInterceptors:
    """
    Decorator that binds one or more interceptors to a class or method.

    Interceptors apply logic before/after route handlers, similar to middleware but
    scoped to controller or method level. Can be chained and combined with global ones.

    - When used on a **class**, it applies to all methods.
    - When used on a **method**, it applies only to that method.

    Example:
    ```python
    @UseInterceptors(MyInterceptor)
    class MyController:
        @UseInterceptors(OtherInterceptor)
        def get_user(self): ...
    ```

    :param interceptors: List of interceptor classes or instances.
    """

    def __init__(self, *interceptors: Union[Type, object]):
        self.interceptors = interceptors

    def __call__(
        self,
        target: Union[Callable, Type],
        key: Optional[str] = None,
        descriptor: Optional[Callable] = None,
    ) -> Union[Callable, Type]:
        """
        Apply the interceptors metadata to the given class or method.

        :param target: The decorated class or method.
        :param key: The method name (only for methods).
        :param descriptor: The method function (only for methods).
        :return: The original target.
        """
        if descriptor:
            # Method-level decorator
            validate_each(target.__class__, self.interceptors, is_interceptor_valid, "@UseInterceptors", "interceptor")
            extend_array_metadata(INTERCEPTORS_METADATA, list(self.interceptors), descriptor)
            return descriptor

        # Class-level decorator
        validate_each(target, self.interceptors, is_interceptor_valid, "@UseInterceptors", "interceptor")
        extend_array_metadata(INTERCEPTORS_METADATA, list(self.interceptors), target)
        return target
