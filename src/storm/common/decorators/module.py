# src/storm/core/module.py

def Module(imports=None, providers=None, controllers=None):
    """
    Registers a module with its imports, providers, and controllers.

    :param imports: List of imported modules
    :param providers: List of providers (services)
    :param controllers: List of controllers
    :return: The decorated class as a module
    """
    def decorator(cls):
        cls.imports = imports or []
        cls.providers = providers or []
        cls.controllers = controllers or []
        return cls
    return decorator
