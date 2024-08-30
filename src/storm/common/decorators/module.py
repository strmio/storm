from storm.core.module import ModuleBase


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
            module_cls=cls
        )
        return module

    return decorator
