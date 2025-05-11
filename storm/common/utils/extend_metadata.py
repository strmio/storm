# storm/common/utils/extend_metadata.py

from storm.core.di.reflect import Reflect


def extend_array_metadata(key: str, values: list, target):
    """
    Extends an existing metadata list by appending new values to the same key.

    :param key: Metadata key to extend.
    :param values: List of values to add.
    :param target: Function or class to which metadata applies.
    """
    existing = Reflect.get_metadata(key, target) or []
    Reflect.define_metadata(key, existing + values, target)
