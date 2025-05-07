# storm/decorators/apply_decorators.py

from typing import Any, Callable, Optional


class ApplyDecorators:
    """
    Utility class to compose and apply multiple decorators
    to a class, method, or property.

    Usage:
        @ApplyDecorators(decorator1, decorator2)
        def my_method(): ...
    """

    def __init__(self, *decorators: Callable):
        """
        :param decorators: A sequence of decorators to apply.
        """
        self.decorators = decorators

    def __call__(self, target: Any, key: Optional[str] = None, descriptor: Any = None) -> Any:
        # Class decorator
        if key is None and descriptor is None:
            for decorator in self.decorators:
                target = decorator(target) or target
            return target

        # Method/property decorator
        for decorator in self.decorators:
            descriptor = decorator(target, key, descriptor) or descriptor
        return descriptor
