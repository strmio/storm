import uuid
from typing import Any, Callable, Optional, TypeVar, Union

T = TypeVar('T')
V = TypeVar('V')


def generate_uid(length: int = 21) -> str:
    """Generate a short unique ID string."""
    return uuid.uuid4().hex[:length]


class ReflectableDecorator:
    """
    Decorator class that stores metadata under a unique key.
    """

    def __init__(self, key: str, transform: Optional[Callable[[Any], Any]] = None):
        """
        :param key: Unique key used to store metadata.
        :param transform: Optional transformation function for the value.
        """
        self.KEY = key
        self.transform = transform or (lambda x: x)

    def __call__(self, value: Any = None) -> Callable:
        """
        Returns a decorator that attaches metadata to the decorated target.

        :param value: Metadata value to store.
        :return: A decorator function.
        """
        def decorator(target):
            metadata = getattr(target, '__storm_metadata__', {})
            metadata[self.KEY] = self.transform(value)
            setattr(target, '__storm_metadata__', metadata)
            return target
        return decorator


class Reflector:
    """
    Reflection utility for creating decorators and reading metadata in Storm.
    """

    @staticmethod
    def create_decorator(
        key: Optional[str] = None,
        transform: Optional[Callable[[T], V]] = None,
    ) -> ReflectableDecorator:
        """
        Create a decorator that stores metadata under a unique key.

        :param key: Custom metadata key. If not provided, a random UID is used.
        :param transform: Optional function to transform the metadata value.
        :return: A ReflectableDecorator instance.
        """
        return ReflectableDecorator(key or generate_uid(), transform)

    @staticmethod
    def get(key_or_decorator: Union[str, ReflectableDecorator], target: Any) -> Any:
        """
        Retrieve metadata from a target using a key or a ReflectableDecorator.

        :param key_or_decorator: The metadata key or decorator object.
        :param target: The target class or function to retrieve metadata from.
        :return: The stored metadata value, or None if not found.
        """
        key = key_or_decorator.KEY if isinstance(key_or_decorator, ReflectableDecorator) else key_or_decorator
        return getattr(target, '__storm_metadata__', {}).get(key)

    @staticmethod
    def get_all(key_or_decorator: Union[str, ReflectableDecorator], targets: list[Any]) -> list[Any]:
        """
        Retrieve metadata from multiple targets.

        :param key_or_decorator: The metadata key or decorator object.
        :param targets: List of target classes or functions.
        :return: List of metadata values (could include None).
        """
        return [Reflector.get(key_or_decorator, t) for t in targets]

    @staticmethod
    def get_all_and_merge(key_or_decorator: Union[str, ReflectableDecorator], targets: list[Any]) -> Any:
        """
        Merge metadata from multiple targets. Arrays are concatenated,
        dictionaries are merged, primitives are grouped.

        :param key_or_decorator: The metadata key or decorator object.
        :param targets: List of decorated objects.
        :return: A merged result of all metadata values.
        """
        items = [v for v in Reflector.get_all(key_or_decorator, targets) if v is not None]

        if not items:
            return [] if isinstance(items, list) else {}

        if all(isinstance(v, list) for v in items):
            return sum(items, [])
        elif all(isinstance(v, dict) for v in items):
            merged = {}
            for d in items:
                merged.update(d)
            return merged
        return items

    @staticmethod
    def get_all_and_override(key_or_decorator: Union[str, ReflectableDecorator], targets: list[Any]) -> Any:
        """
        Return the first defined metadata value found across multiple targets.

        :param key_or_decorator: The metadata key or decorator object.
        :param targets: List of decorated objects.
        :return: The first non-None metadata value found.
        """
        for target in targets:
            val = Reflector.get(key_or_decorator, target)
            if val is not None:
                return val
        return None
