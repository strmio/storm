
def Get(path):
    """Decorator to define a GET route."""
    def decorator(func):
        func.is_route = True
        func._route = {"method": "GET", "path": path}  # Attach route metadata
        func.route_method = "GET"
        func.route_path = path  # Attach route path
        return func
    return decorator

# def Post(path):
#     return route('POST', path)

# def Put(path):
#     return route('PUT', path)

# def Delete(path):
#     return route('DELETE', path)
