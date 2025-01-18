from inspect import signature, Parameter

from storm.common import execution_context
from storm.common.decorators.param import Params

class ParamsResolver:
    """
    A class responsible for resolving handler arguments, including instances of Params.
    """
    @staticmethod
    async def resolve(handler, request):
        """
        Resolves all arguments for the given handler function.

        :param handler: The handler function to inspect.
        :param request: The incoming request object.
        :return: A dictionary of resolved arguments for the handler.
        """
        # Get the handler's signature
        sig = signature(handler)
        resolved_args = {}

        # Get the current request from the execution context
        context = execution_context.get()
        route_params = context.get("request", {}).get("params", {})

        for param_name, param in sig.parameters.items():
            if param.default is not Parameter.empty and isinstance(param.default, Params):
                # Resolve the Params object using its resolve method
                resolved_args[param_name] = param.default.resolve()
            elif param_name in route_params:
                # Use route parameters directly if available
                resolved_args[param_name] = route_params[param_name]
            else:
                # Add default or empty values for other parameters
                resolved_args[param_name] = param.default if param.default is not Parameter.empty else None

        return resolved_args
