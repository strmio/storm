from storm.common.services.logger import Logger
import re


class Router:
    def __init__(self):
        self.routes = {}
        self.logger = Logger()

    def add_route(self, method, path, handler):
        """
        Registers a new route with the specified HTTP method and path.

        :param method: The HTTP method (GET, POST, etc.)
        :param path: The URL path (e.g., '/users/:id')
        :param handler: The function to handle requests to this route
        """
        self.logger.info(f"Adding route: {method} {path}")
        path_regex = self._path_to_regex(path)
        self.routes[(method, path_regex)] = handler

    def resolve(self, method, path):
        """
        Resolves a route by matching the method and path against registered routes.

        :param method: The HTTP method (GET, POST, etc.)
        :param path: The URL path from the incoming request
        :return: The handler function and any extracted parameters
        """
        self.logger.info(f"Resolving route for: {method} {path}")
        for (route_method, path_regex), handler in self.routes.items():
            if route_method == method and re.match(path_regex, path):
                self.logger.info(f"Matched route: {method} {path}")
                params = self._extract_params(path_regex, path)
                return handler, params
        self.logger.error(f"No route found for: {method} {path}")
        raise ValueError(f"No route found for {method} {path}")

    def _path_to_regex(self, path):
        """
        Converts a path with parameters (e.g., '/users/:id') into a regular expression.

        :param path: The URL path
        :return: A regex pattern that matches the path
        """
        return re.sub(r':(\w+)', r'(?P<\1>[^/]+)', path) + r'$'

    def _extract_params(self, path_regex, path):
        """
        Extracts parameters from the URL path based on the regex pattern.

        :param path_regex: The regex pattern of the path
        :param path: The URL path from the incoming request
        :return: A dictionary of extracted parameters
        """
        match = re.match(path_regex, path)
        return match.groupdict() if match else {}
