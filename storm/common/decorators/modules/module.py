from storm.common.interfaces.modules.module_metadata import ModuleMetadata
from storm.common.utils.validate_module_keys import validate_module_keys
from storm.core.di.reflect import Reflect


class Module:
    """
    Decorator that marks a class as a Storm module.

    :param metadata: Dictionary defining module configuration: imports, controllers, providers, exports.
    """

    def __init__(self, metadata: ModuleMetadata):
        self.metadata = metadata
        validate_module_keys(list(metadata.keys()))

    def __call__(self, target: type) -> type:
        for key, value in self.metadata.items():
            Reflect.define_metadata(key, value, target)
        return target
