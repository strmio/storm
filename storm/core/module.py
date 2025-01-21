
class ModuleBase:
    def __init__(
        self, *, controllers=None, providers=None, imports=None, middleware=None, module_cls=None
    ):
        """
        Initialize the module with controllers, providers, imports, and middleware.
        
        :param controllers: List of controller classes.
        :param providers: List of provider (service) classes.
        :param imports: List of other modules to be imported.
        :param middleware: List of middleware classes.
        :param module_cls: Optional custom module class with lifecycle hooks.
        """
        self.controllers = self._initialize_map(controllers)
        self.providers = self._initialize_map(providers)
        self.imports = imports or []
        self.middleware = middleware or []
        self._module_cls = module_cls

        # self._invoke_lifecycle_hook("onInit")
        # self._invoke_lifecycle_hook("onDestroy")

    def _initialize_map(self, items):
        """Create a dictionary with class names as keys and classes as values."""
        return {item.__name__: item for item in (items or [])}

    def _invoke_lifecycle_hook(self, hook_name):
        """Invoke a lifecycle hook if it exists and is callable."""
        if hasattr(self._module_cls, hook_name) and callable(getattr(self._module_cls, hook_name)):
            getattr(self._module_cls, hook_name)(self)

    def register(self, container):
        """
        Register all providers, controllers, and middleware in the container.
        
        :param container: The DI container.
        """
        self._register_imports(container)
        self._register_items(container, self.providers, singleton=True)
        self._register_items(container, self.controllers, singleton=True)
        self._register_items(container, self.middleware, singleton=True)

    def _register_imports(self, container):
        """Register imported modules in the container."""
        for imported_module in self.imports:
            imported_module.register(container)

    def _register_items(self, container, items, singleton):
        """Register items (providers, controllers, or middleware) in the container."""
        for item_name, item_cls in items.items():
            container.register(item_name, item_cls, singleton=singleton)
