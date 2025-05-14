from enum import Enum
from typing import Any, Optional, Protocol, Type, runtime_checkable


class Paramtype(str, Enum):
    BODY = "body"
    QUERY = "query"
    PARAM = "param"
    CUSTOM = "custom"


class ArgumentMetadata:
    """
    Metadata about a route handler argument passed to a pipe.

    :param type: Type of the parameter (e.g. 'body', 'query').
    :param metatype: The original class/type used in the route handler.
    :param data: Optional additional metadata (e.g., name from @Body('name')).
    """

    def __init__(self, type: Paramtype, metatype: Optional[Type] = None, data: Optional[str] = None):
        self.type = type
        self.metatype = metatype
        self.data = data


@runtime_checkable
class PipeTransform(Protocol):
    """
    Protocol for implementing a Pipe. Pipes can transform input before it reaches the handler.
    """

    def transform(self, value: Any, metadata: ArgumentMetadata) -> Any: ...
