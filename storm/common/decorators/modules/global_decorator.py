# storm/common/decorators/core/global_module.py

from storm.common.constants import GLOBAL_MODULE_METADATA
from storm.core.di.reflect import Reflect


class Global:
    """
    Decorator that makes a module global-scoped.

    Once imported into any module, a global-scoped module will be visible
    in all modules. Thereafter, modules that wish to inject a service exported
    from a global module do not need to import the provider module.

    Equivalent to NestJS @Global()

    :return: ClassDecorator
    """

    def __call__(self, target: type) -> type:
        Reflect.define_metadata(GLOBAL_MODULE_METADATA, True, target)
        return target
