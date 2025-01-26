from functools import wraps
from typing import Callable, Union, Type
import inspect

from storm.common.pipes.pipe import Pipe


def UsePipes(*pipes: Union[Type[Pipe], Pipe]):
    """
    Decorator to apply pipes to a route handler.

    :param pipes: One or more Pipe instances or classes to apply.
    """

    def decorator(func: Callable):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            # Inspect function signature to determine parameter metadata
            sig = inspect.signature(func)
            bound_args = sig.bind_partial(*args, **kwargs)
            bound_args.apply_defaults()

            # Apply pipes to each parameter
            for param_name, value in bound_args.arguments.items():
                # Find pipes and transform arguments
                for pipe in pipes:
                    # Instantiate the pipe if it's a class
                    pipe_instance = pipe() if isinstance(pipe, type) else pipe

                    # Create metadata for transformation
                    metadata = {
                        "type": "custom",
                        "data": param_name,
                        "metatype": sig.parameters[param_name].annotation,
                    }

                    # Transform the value
                    value = await pipe_instance.transform(value, metadata)

                # Update the transformed argument
                bound_args.arguments[param_name] = value

            # Call the original function with transformed arguments
            return await func(*bound_args.args, **bound_args.kwargs)

        return wrapper

    return decorator
