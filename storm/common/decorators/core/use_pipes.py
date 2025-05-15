from typing import Callable, Optional, Type, Union

from storm.common.constants import PIPES_METADATA
from storm.common.interfaces.features.pipe_transform import PipeTransform
from storm.common.utils.extend_metadata import extend_array_metadata
from storm.common.utils.shared import is_function
from storm.common.utils.validate_each import validate_each


def is_pipe_valid(pipe) -> bool:
    """
    Validates whether the given object is a valid pipe for use with the @UsePipes decorator.

    A valid pipe must meet one of the following conditions:
    - It is a class or function reference that defines a `transform` method (either directly or on an instance).
    - It is an instance that has a callable `transform` method.

    This validation allows both class-based pipes and instantiated pipes.

    Examples of valid pipes:
    - A class: `class MyPipe: def transform(self, value, metadata): ...`
    - An instance: `MyPipe()`
    - A factory function returning a pipe object

    :param pipe: The object to validate (can be a class, function, or instance).
    :return: True if the object qualifies as a pipe, False otherwise.
    """
    if not pipe:
        return False

    # Class or function reference
    if is_function(pipe):
        return hasattr(pipe, "transform") or hasattr(pipe(), "transform")

    # Instance
    return hasattr(pipe, "transform") and callable(getattr(pipe, "transform", None))


class UsePipes:
    """
    Decorator that binds pipes to the scope of the controller or method.

    Can be applied to:
    - Class: applies the pipes to all methods of the class
    - Method: applies the pipes to the specific method

    Example:
        @UsePipes(MyPipe)
        class MyController:
            ...

        @UsePipes(MyPipe)
        def my_method(...):
            ...
    """

    def __init__(self, *pipes: Union[PipeTransform, Callable]):
        self.pipes = list(pipes)

    def __call__(
        self,
        target: Union[Callable, Type],
        key: Optional[str] = None,
        descriptor: Optional[Callable] = None,
    ) -> Union[Callable, Type]:
        if descriptor:
            extend_array_metadata(PIPES_METADATA, list(self.pipes), descriptor)
            return descriptor

        validate_each({"name": getattr(target, "__name__", target.__class__.__name__)}, self.pipes, is_pipe_valid, "@UsePipes", "pipe")
        extend_array_metadata(PIPES_METADATA, list(self.pipes), target)
        return target
