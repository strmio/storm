from inspect import Parameter, signature

from storm.common.decorators.body import Body
from storm.common.decorators.headers import Headers
from storm.common.decorators.optional import OptionalMeta
from storm.common.decorators.param import Param
from storm.common.decorators.query_params import Query
from storm.common.execution_context import execution_context


class ParamsResolver:
    """
    A class responsible for resolving handler arguments, including instances of Param, Query, Body, and Optional.
    """

    @staticmethod
    async def resolve(handler, request):
        """
        Resolves all arguments for the given handler function.

        :param handler: The handler function to inspect.
        :param request: The incoming request object.
        :return: A dictionary of resolved arguments for the handler.
        """
        resolved_args = {}
        request = execution_context.get_request()
        route_params = request.get_params()
        query_params = request.get_query_params()
        body = request.get_body()

        for param_name, param in signature(handler).parameters.items():
            resolved_args[param_name] = await ParamsResolver._resolve_param(param, route_params, query_params, body)

        return resolved_args

    @staticmethod
    async def _resolve_param(param, route_params, query_params, body):
        """
        Resolves a single parameter based on its type and context.

        :param param: The parameter to resolve.
        :param route_params: Parameters from the route.
        :param query_params: Query parameters from the request.
        :param body: Body content from the request.
        :return: The resolved value for the parameter.
        """
        if param.default is not Parameter.empty:
            return await ParamsResolver._resolve_with_default(param, route_params, query_params, body)
        return ParamsResolver._resolve_without_default(param.name, route_params, query_params, body)

    @staticmethod
    async def _resolve_with_default(param, route_params, query_params, body):
        """
        Resolves a parameter with a default value.

        :param param: The parameter to resolve.
        :param route_params: Parameters from the route.
        :param query_params: Query parameters from the request.
        :param body: Body content from the request.
        :return: The resolved value for the parameter.
        """
        if isinstance(param.default, (Param, Query, Body, Headers)):
            return await param.default.resolve()
        if isinstance(param.default, OptionalMeta):
            return param.default.default
        return param.default

    @staticmethod
    def _resolve_without_default(param_name, route_params, query_params, body):
        """
        Resolves a parameter without a default value.

        :param param_name: The name of the parameter.
        :param route_params: Parameters from the route.
        :param query_params: Query parameters from the request.
        :param body: Body content from the request.
        :return: The resolved value for the parameter or None if not found.
        """
        if param_name in route_params:
            return route_params[param_name]
        if param_name in query_params:
            return query_params[param_name]
        if param_name in body:
            return body[param_name]
        return None
