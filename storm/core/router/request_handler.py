from urllib.parse import parse_qs
from .router import Router

class RequestHandler:
    """
    RequestHandler class that handles incoming HTTP requests, resolves
    the appropriate route, and manages query and path parameters.

    Attributes:
        router (Router): An instance of the Router class used to resolve routes.
    """

    def __init__(self, router):
        """
        Initialize the RequestHandler with a Router instance.

        Args:
            router (Router): An instance of the Router class.
        """
        self.router = router

    async def handle_request(self, method, path, query_string=None):
        """
        Handles an incoming HTTP request by resolving the appropriate route
        and managing query parameters.

        Args:
            method (str): The HTTP method (e.g., 'GET', 'POST').
            path (str): The URL path.
            query_string (str, optional): The query string (e.g., 'filter=active').

        Returns:
            tuple: A tuple containing the response and HTTP status code.

        Raises:
            ValueError: If no matching route is found.
            KeyError: If required parameters are missing.
        """
        try:
            handler, params = self.router.resolve(method, path)
            query_params = parse_qs(query_string) if query_string else {}
            params.update(query_params)
            return await handler(params), 200
        except ValueError as e:
            return {"error": "Route not found", "details": str(e)}, 404
        except KeyError as e:
            return {"error": "Missing parameter", "details": str(e)}, 400
