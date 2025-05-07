# storm/decorators/set_metadata.py

from storm.core.di.reflect import Reflect


class SetMetadata:
    """
    Decorator class that assigns metadata to a class or method.

    Equivalent to NestJS's `SetMetadata`.

    :param metadata_key: Key under which to store metadata.
    :param metadata_value: Value to associate with the key.
    :example:
        @SetMetadata("roles", ["admin"])
        class AdminController: ...
    """

    def __init__(self, metadata_key, metadata_value):
        self.metadata_key = metadata_key
        self.metadata_value = metadata_value
        self.KEY = metadata_key

    def __call__(self, target):
        Reflect.define_metadata(self.metadata_key, self.metadata_value, target)
        return target
