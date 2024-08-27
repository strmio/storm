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
