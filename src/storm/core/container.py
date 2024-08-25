import inspect

class Container:
    def __init__(self):
        self._services = {}
        self._singletons = {}

    def register(self, name, service, singleton=True):
        """
        Register a service in the container.
        :param name: Name of the service.
        :param service: The service class or function.
        :param singleton: Boolean indicating if the service should be a singleton.
        """
        self._services[name] = {
            'service': service,
            'singleton': singleton,
        }

    def resolve(self, name):
        """
        Resolve a service by name, automatically resolving dependencies.
        :param name: Name of the service to resolve.
        :return: The instance of the service.
        """
        if name in self._singletons:
            return self._singletons[name]

        service_meta = self._services.get(name)
        if not service_meta:
            raise Exception(f"Service {name} not found.")

        service = service_meta['service']

        if inspect.isclass(service):
            # Automatically resolve dependencies for the class's __init__ method
            init_params = inspect.signature(service.__init__).parameters
            dependencies = {
                param: self.resolve(param_class.annotation.__name__)
                for param, param_class in init_params.items()
                if param != 'self' and param_class.annotation != inspect.Parameter.empty
            }
            instance = service(**dependencies)
        else:
            instance = service

        if service_meta['singleton']:
            self._singletons[name] = instance

        return instance
