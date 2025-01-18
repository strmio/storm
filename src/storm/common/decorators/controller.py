from storm.core.controller import ControllerBase
import inspect


def Controller(base_path, middleware=[]):
    """
    A decorator for registering a controller and its routes.

    :param base_path: The base path for the controller's routes.
    :param middleware: Optional middleware to be applied to the controller's routes.
    """
    def decorator(cls):
        # Modify the class initialization to handle ControllerBase initialization
        original_init = cls.__init__
        # Access the function's signature
        signature = inspect.signature(original_init)

        def new_init(self, *args, **kwargs):
            # Initialize ControllerBase automatically
            ControllerBase.__init__(self, base_path, middleware)

            # Call the original class's __init__, if needed (in case controller has custom logic)

            # Prepare arguments for the original __init__ method
            bound_args = signature.bind_partial(*args, **kwargs)
            for name, param in signature.parameters.items():
                if name not in bound_args.arguments:
                    # Use the annotation if callable, otherwise default value
                    if param.annotation is not inspect.Parameter.empty and callable(param.annotation):
                        bound_args.arguments[name] = param.annotation()
                    elif param.default is not inspect.Parameter.empty:
                        bound_args.arguments[name] = param.default

            # Call the original class's __init__ with prepared arguments
            original_init(self, *bound_args.args, **bound_args.kwargs)

            # Automatically register routes
            for attr_name in dir(self):
                attr = getattr(self, attr_name)
                if callable(attr) and hasattr(attr, '_route'):
                    self.router.add_route(
                        attr.route_method, base_path + attr.route_path, attr)

        cls.__init__ = new_init  # Replace the constructor with the new init
        return cls
    return decorator
