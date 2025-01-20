from storm.common.services.logger import Logger
import re


class Router:
    def __init__(self):
        self.static_routes = {}
        self.dynamic_routes = {}
        self.logger = Logger(self.__class__.__name__)

    def add_route(self, method, path, handler):
        """
        Registers a new route with the specified HTTP method and path.

        :param method: The HTTP method (GET, POST, etc.)
        :param path: The URL path (e.g., '/users/:id')
        :param handler: The function to handle requests to this route
        """
        path_regex = self._path_to_regex(path)
        if ':' in path:
            self.dynamic_routes[(method, path_regex)] = handler
        else:
            self.static_routes[(method, path)] = handler

    def add_static_route_from_controller_router(self, method_path, handler):
        """
        Registers a new static route with the specified HTTP method and path.

        :param method: The HTTP method (GET, POST, etc.)
        :param path: The URL path (e.g., '/users/:id')
        :param handler: The function to handle requests to this route
        """
        self.static_routes[method_path] = handler
    
    def add_dynamic_route_from_controller_router(self, method_path, handler):
        """
        Registers a new dynamic route with the specified HTTP method and path.

        :param method: The HTTP method (GET, POST, etc.)
        :param path: The URL path (e.g., '/users/:id')
        :param handler: The function to handle requests to this route
        """
        self.dynamic_routes[method_path] = handler

    def resolve(self, method, path):
        """
        Resolves a route by matching the method and path against registered routes.

        :param method: The HTTP method (GET, POST, etc.)
        :param path: The URL path from the incoming request
        :return: The handler function and any extracted parameters
        """
        if (method, path) in self.static_routes:
            return self.static_routes[(method, path)], {}
        for (route_method, path_regex), handler in self.dynamic_routes.items():
            if route_method == method and re.match(path_regex, path):
                params = self._extract_params(path_regex, path)
                return handler, params
        raise ValueError(f"No route found for {method} {path}")


    def _path_to_regex(self, path):
        """
        Converts a path with parameters (e.g., '/users/:id') into a regular expression.

        :param path: The URL path
        :return: A regex pattern that matches the path
        """
        return re.sub(r':(\w+)', r'(?P<\1>[^/]+)', path) + r'/?$'

    def _extract_params(self, path_regex, path):
        """
        Extracts parameters from the URL path based on the regex pattern.

        :param path_regex: The regex pattern of the path
        :param path: The URL path from the incoming request
        :return: A dictionary of extracted parameters
        """
        match = re.match(path_regex, path)
        return match.groupdict() if match else {}

    def get_static_routes(self):
        """
        Retrieves all static routes.

        :return: A dictionary of static routes with their handlers
        """
        return self.static_routes

    def get_dynamic_routes(self):
        """
        Retrieves all dynamic routes.

        :return: A dictionary of dynamic routes with their handlers
        """
        return self.dynamic_routes
