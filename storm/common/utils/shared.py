import re
from typing import Any, Union


def is_undefined(obj: Any) -> bool:
    """Checks if an object is undefined (not applicable in Python)."""
    return obj is None  # In Python, `None` is the closest equivalent.


def is_object(fn: Any) -> bool:
    """Checks if a value is an object (but not None)."""
    return fn is not None and isinstance(fn, object)


def is_plain_object(fn: Any) -> bool:
    """Checks if a value is a plain object (not an instance of a class)."""
    if not is_object(fn):
        return False
    proto = getattr(fn, "__class__", None)
    if proto is None:
        return True
    return isinstance(fn, dict) and proto is dict


def add_leading_slash(path: Union[str, None]) -> str:
    """Ensures a string starts with a leading slash."""
    if isinstance(path, str):
        return path if path.startswith("/") else "/" + path
    return ""


def normalize_path(path: Union[str, None]) -> str:
    """Normalizes a path by removing duplicate slashes and ensuring it starts with '/'."""
    if not path:
        return "/"
    path = re.sub(r"/{2,}", "/", path.strip("/"))
    return "/" + path


def strip_end_slash(path: str) -> str:
    """Removes the trailing slash from a path if it exists."""
    return path.rstrip("/") if path.endswith("/") else path


def is_function(val: Any) -> bool:
    """Checks if a value is a function."""
    return callable(val)


def is_string(val: Any) -> bool:
    """Checks if a value is a string."""
    return isinstance(val, str)


def is_number(val: Any) -> bool:
    """Checks if a value is a number."""
    return isinstance(val, (int, float))


def is_constructor(val: Any) -> bool:
    """Checks if a value is '__init__' (not needed in Python)."""
    return val == "__init__"


def is_nil(val: Any) -> bool:
    """Checks if a value is None or undefined."""
    return val is None


def is_empty(array: Any) -> bool:
    """Checks if an array (or list) is empty."""
    return not array or len(array) == 0


def is_symbol(val: Any) -> bool:
    """Checks if a value is a symbol (not applicable in Python)."""
    return isinstance(val, (bytes, bytearray))  # Symbols don’t exist in Python, but bytes can be similar.


def deduplicate_preserve_order(seq):
    seen = set()
    return [x for x in seq if not (x in seen or seen.add(x))]
