from typing import Optional, Type, TypedDict


class ArgumentMetadata(TypedDict):
    """
    Represents metadata about an argument in the handler.
    """

    type: str  # 'body', 'query', 'param', or 'custom'
    metatype: Optional[Type[object]]  # The expected Python type of the argument
    data: Optional[str]  # Additional data or identifier for the argument
