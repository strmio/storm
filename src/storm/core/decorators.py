def Injectable(singleton=True):
    """
    Mark a class as injectable.
    :param singleton: Boolean indicating if the service should be a singleton.
    """
    def wrapper(cls):
        cls.__injectable__ = True
        cls.__singleton__ = singleton
        return cls
    return wrapper


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
