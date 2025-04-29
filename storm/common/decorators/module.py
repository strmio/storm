from storm.common.constants import MODULE_WATERMARK
from storm.core.module import ModuleBase
from storm.core.reflector import Reflector


def Module(imports=None, providers=None, controllers=None):
    """
    Registers a module with its imports, providers, and controllers.

    :param imports: List of imported modules
    :param providers: List of providers (services)
    :param controllers: List of controllers
    :return: The decorated class as a module
    """

    def decorator(cls):
        module = ModuleBase(
            imports=imports or [],
            providers=providers or [],
            controllers=controllers or [],
            module_cls=cls,
        )
        module.__name__ = cls.__name__
        Reflector.set_metadata(module, "__module__", module)
        Reflector.set_metadata(module, "__imports__", imports or [])
        Reflector.set_metadata(module, "__providers__", providers or [])
        Reflector.set_metadata(module, "__controllers__", controllers or [])
        Reflector.set_watermark(module, MODULE_WATERMARK)
        return module

    return decorator
