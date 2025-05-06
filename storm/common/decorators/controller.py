def Controller(base_path="", middleware=None):
    """
    A decorator for registering a controller and its routes.

    :param base_path: The base path for the controller's routes.
    :param middleware: Optional middleware to be applied to the controller's routes.
    """

    if middleware is None:
        middleware = []

    def decorator(cls):
        cls.__base_path__ = base_path
        cls.__middleware__ = middleware
        return cls

    return decorator
