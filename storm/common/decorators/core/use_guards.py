from typing import Callable, Optional, Type, Union

from storm.common.constants import GUARDS_METADATA
from storm.common.utils.extend_metadata import extend_array_metadata
from storm.common.utils.shared import is_function
from storm.common.utils.validate_each import validate_each


def is_guard_valid(guard) -> bool:
    if not guard:
        return False

    # Class or function reference
    if is_function(guard):
        return hasattr(guard, "can_activate") or hasattr(guard(), "can_activate")

    # Instance
    return hasattr(guard, "can_activate") and callable(getattr(guard, "can_activate", None))


class UseGuards:
    """
    Decorator that binds guards to a controller class or a method.

    - At the controller level: applies the guard to all handlers.
    - At the method level: applies the guard to that method only.

    Usage:
        @UseGuards(MyGuard)
        class MyController: ...

        @UseGuards(AuthGuard)
        def handler(...): ...
    """

    def __init__(self, *guards: Union[Type, object]):
        self.guards = guards

    def __call__(
        self,
        target: Union[Callable, Type],
        key: Optional[str] = None,
        descriptor: Optional[Callable] = None,
    ) -> Union[Callable, Type]:
        if descriptor:
            extend_array_metadata(GUARDS_METADATA, list(self.guards), descriptor)
            return descriptor

        validate_each({"name": getattr(target, "__name__", target.__class__.__name__)}, self.guards, is_guard_valid, "@UseGuards", "guard")
        extend_array_metadata(GUARDS_METADATA, list(self.guards), target)
        return target
