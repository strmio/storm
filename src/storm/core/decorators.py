def Injectable(cls):
    cls.__injectable__ = True
    return cls

def Controller(route):
    def decorator(cls):
        cls.__route__ = route
        return cls
    return decorator
