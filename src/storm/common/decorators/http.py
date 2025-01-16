
def Get(path=""):
    """Decorator to define a GET route."""
    def decorator(func):
        func.is_route = True
        func._route = {"method": "GET", "path": path}  # Attach route metadata
        func.route_method = "GET"
        func.route_path = path  # Attach route path
        return func
    return decorator


def Post(path=""):
    """Decorator to define a POST route."""
    def decorator(func):
        func.is_route = True
        func._route = {"method": "POST", "path": path}  # Attach route metadata
        func.route_method = "POST"
        func.route_path = path  # Attach route path
        return func
    return decorator


def Put(path=""):
    """Decorator to define a POST route."""
    def decorator(func):
        func.is_route = True
        func._route = {"method": "PUT", "path": path}  # Attach route metadata
        func.route_method = "PUT"
        func.route_path = path  # Attach route path
        return func
    return decorator


def Delete(path=""):
    """Decorator to define a POST route."""
    def decorator(func):
        func.is_route = True
        # Attach route metadata
        func._route = {"method": "DELETE", "path": path}
        func.route_method = "DELETE"
        func.route_path = path  # Attach route path
        return func
    return decorator
