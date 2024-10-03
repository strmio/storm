import inspect
from storm.core.container import Container

class Injector:
    def __init__(self, container: Container):
        self.container = container

    def inject(self, cls):
        """
        Injects dependencies into the given class by resolving its constructor arguments.
        :param cls: The class to inject dependencies into.
        :return: An instance of the class with dependencies resolved.
        """
        constructor_params = inspect.signature(cls.__init__).parameters
        dependencies = {}

        for param, param_info in constructor_params.items():
            if param != 'self' and param_info.annotation != inspect.Parameter.empty:
                dependency_name = param_info.annotation.__name__
                dependencies[param] = self.container.resolve(dependency_name)

        return cls(**dependencies)

    def inject_into_function(self, func):
        """
        Injects dependencies into a function's parameters.
        :param func: The function to inject dependencies into.
        :return: A wrapped function with injected dependencies.
        """
        func_params = inspect.signature(func).parameters
        dependencies = {}

        for param, param_info in func_params.items():
            if param_info.annotation != inspect.Parameter.empty:
                dependency_name = param_info.annotation.__name__
                dependencies[param] = self.container.resolve(dependency_name)

        def wrapper(*args, **kwargs):
            return func(*args, **dependencies, **kwargs)

        return wrapper