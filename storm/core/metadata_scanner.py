import inspect
from types import FunctionType
from typing import Any, Callable, Type


class MetadataScanner:
    def __init__(self):
        self._cached_scanned_classes: dict[type, list[str]] = {}

    def scan_from_class(
        self,
        cls: Type,
        callback: Callable[[str], Any],
    ) -> list[Any]:
        """
        Iterates through all method names in the class (and parents),
        calls `callback` for each valid method name, and returns results.
        """
        result = []
        visited = set()

        for name in self.get_all_method_names(cls):
            if name in visited:
                continue
            visited.add(name)
            value = callback(name)
            if value is not None:
                result.append(value)
        return result

    def get_all_method_names(self, cls: Type | None) -> list[str]:
        """
        Returns all method names (excluding dunder methods and properties).
        """
        if cls is None:
            return []

        if cls in self._cached_scanned_classes:
            return self._cached_scanned_classes[cls]

        method_names = []
        visited = set()

        for base in inspect.getmro(cls):
            if base is object:
                break

            for name, member in base.__dict__.items():
                if name in visited:
                    continue
                visited.add(name)

                if isinstance(member, (FunctionType, classmethod, staticmethod)) and not name.startswith("__"):
                    method_names.append(name)

        self._cached_scanned_classes[cls] = method_names
        return method_names
