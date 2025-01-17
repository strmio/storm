from functools import wraps

def Request(param_name):
    """Decorator to pass the request data as a parameter to the function."""
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            # Check if the function has a `request` attribute
            if hasattr(func, "request"):
                # Inject the `request` data into kwargs
                kwargs[param_name] = func.request
            return func(*args, **kwargs)
        return wrapper
    return decorator

Req = Request
