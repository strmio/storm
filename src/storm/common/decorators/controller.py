def Controller(route):
    """
    Mark a class as a controller and associate it with a route.
    :param route: Base route for the controller.
    """
    def wrapper(cls):
        cls.__route__ = route
        cls.__is_controller__ = True
        return cls
    return wrapper
