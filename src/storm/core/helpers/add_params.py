import inspect
from functools import wraps

def add_params(func, **new_params):
    # Get the original signature
    original_signature = inspect.signature(func)
    original_parameters = original_signature.parameters

    # Create a dictionary of parameters, allowing modification of existing ones
    updated_parameters = {}

    # Add or update existing parameters
    for name, param in original_parameters.items():
        if name in new_params:
            # Update the default value if the parameter already exists
            updated_parameters[name] = param.replace(default=new_params[name])
        else:
            updated_parameters[name] = param

    # Add new parameters that aren't in the original signature
    for name, value in new_params.items():
        if name not in updated_parameters:
            updated_parameters[name] = inspect.Parameter(
                name,
                inspect.Parameter.KEYWORD_ONLY,  # Add as keyword-only parameter
                default=value
            )

    # Create a new signature with updated parameters
    new_signature = original_signature.replace(parameters=updated_parameters.values())

    # Define a wrapper function
    @wraps(func)
    def wrapper(*args, **kwargs):
        return func(*args, **kwargs)

    # Update the wrapper's signature
    wrapper.__signature__ = new_signature

    return wrapper
