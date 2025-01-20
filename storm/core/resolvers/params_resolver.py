from inspect import signature, Parameter
from storm.common.execution_context import execution_context
from storm.common.decorators.param import Param
from storm.common.decorators.query_params import Query
from storm.common.decorators.body import Body

class ParamsResolver:
    """
    A class responsible for resolving handler arguments, including instances of Param, Query, and Body.
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
        query_params = context.get("request", {}).get("query_params", {})
        body = context.get("request", {}).get("body", {})

        for param_name, param in sig.parameters.items():
            if param.default is not Parameter.empty:
                if isinstance(param.default, Param):
                    # Resolve the Param object asynchronously
                    resolved_args[param_name] = await param.default.resolve()
                elif isinstance(param.default, Query):
                    # Resolve the Query object asynchronously
                    resolved_args[param_name] = await param.default.resolve()
                elif isinstance(param.default, Body):
                    # Resolve the Body object asynchronously
                    resolved_args[param_name] = await param.default.resolve()
            elif param_name in route_params:
                # Use route parameters directly if available
                resolved_args[param_name] = route_params[param_name]
            elif param_name in query_params:
                # Use query parameters directly if available
                resolved_args[param_name] = query_params[param_name]
            elif param_name in body:
                # Use body parameters directly if available
                resolved_args[param_name] = body[param_name]
            else:
                # Add default or empty values for other parameters
                resolved_args[param_name] = param.default if param.default is not Parameter.empty else None

        return resolved_args