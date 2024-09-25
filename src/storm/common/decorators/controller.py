from storm.core.controller import ControllerBase


def Controller(base_path, middleware=[]):
    """
    A decorator for registering a controller and its routes.
    
    :param base_path: The base path for the controller's routes.
    :param middleware: Optional middleware to be applied to the controller's routes.
    """
    def decorator(cls):
        # Modify the class initialization to handle ControllerBase initialization
        original_init = cls.__init__

        def new_init(self, *args, **kwargs):
            # Initialize ControllerBase automatically
            ControllerBase.__init__(self, base_path, middleware)

            # Call the original class's __init__, if needed (in case controller has custom logic)
            original_init(self, *args, **kwargs)

            # Automatically register routes
            for attr_name in dir(self):
                attr = getattr(self, attr_name)
                if callable(attr) and hasattr(attr, 'route_method'):
                    self.add_route(attr.route_method, attr.route_path, attr)

        cls.__init__ = new_init  # Replace the constructor with the new init
        return cls
    return decorator
