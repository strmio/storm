from typing import Any, Callable


class InvalidDecoratorItemException(Exception):
    """
    Raised when a decorator receives an invalid item (e.g., pipe, guard, etc.).
    """

    def __init__(self, decorator: str, item: str, context: str):
        message = f"Invalid {item} passed to {decorator}() decorator ({context})."
        super().__init__(message)


def validate_each(
    context: Any,
    arr: list,
    predicate: Callable,
    decorator: str,
    item: str,
) -> bool:
    """
    Validates that each item in `arr` satisfies the `predicate`. Raises
    InvalidDecoratorItemException if any item fails the predicate.

    :param context: The class or function using the decorator.
    :param arr: The array of items to validate.
    :param predicate: Function used to validate each item.
    :param decorator: Name of the decorator for error messages.
    :param item: Description of the item being validated.
    :return: True if all items pass the predicate.
    """
    context_name = context.get("name") if isinstance(context, dict) else getattr(context, "__name__", None) or context.__class__.__name__

    if any(not predicate(el) for el in arr):
        raise InvalidDecoratorItemException(decorator, item, context_name)

    return True
