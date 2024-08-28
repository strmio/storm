class Module:
    def __init__(self, controllers=[], providers=[], imports=[], middleware=[]):
        """
        Initialize the module with controllers, providers, imports, and middleware.
        :param controllers: List of controller classes.
        :param providers: List of provider (service) classes.
        :param imports: List of other modules to be imported.
        :param middleware: List of middleware classes.
        """
        self.controllers = controllers
        self.providers = providers
        self.imports = imports
        self.middleware = middleware

    def register(self, container):
        """
        Register all providers, controllers, and middleware in the container.
        :param container: The DI container.
        """
        # Register imported modules first
        for imported_module in self.imports:
            imported_module.register(container)

        # Register providers
        for provider in self.providers:
            name = provider.__name__
            container.register(name, provider, singleton=getattr(provider, '__singleton__', True))

        # Register controllers with middleware
        for controller in self.controllers:
            name = controller.__name__
            container.register(name, controller, singleton=True)

        # Register middleware
        for middleware in self.middleware:
            container.register(middleware.__name__, middleware, singleton=True)
