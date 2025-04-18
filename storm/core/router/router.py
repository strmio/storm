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
        if ":" in path:
            self.dynamic_routes[(method, path, path_regex)] = handler
        else:
            self.static_routes[(method, path)] = handler

    def resolve(self, method, path):
        """
        Resolves a route by matching the method and path against registered routes.

        :param method: The HTTP method (GET, POST, etc.)
        :param path: The URL path from the incoming request
        :return: The handler function and any extracted parameters
        """
        if (method, path) in self.static_routes:
            return self.static_routes[(method, path)], {}

        # Sort dynamic routes by specificity
        sorted_dynamic_routes = sorted(
            self.dynamic_routes.items(),
            key=lambda item: self._specificity(item[0][1]),
            reverse=True,
        )

        for (route_method, original_path, path_regex), handler in sorted_dynamic_routes:
            if route_method == method and re.match(path_regex, path):
                params = self._extract_params(path_regex, path)
                return handler, params

        raise ValueError(f"No route found for {method} {path}")

    def _specificity(self, path):
        """
        Calculates the specificity of a path based on static segments.

        :param path: The URL path
        :return: Specificity score (higher is more specific)
        """
        return len(
            [segment for segment in path.split("/") if not segment.startswith(":")]
        )

    def _path_to_regex(self, path):
        """
        Converts a path with parameters (e.g., '/users/:id') into a regular expression.

        :param path: The URL path
        :return: A regex pattern that matches the path
        """
        return re.sub(r":(\w+)", r"(?P<\1>[^/]+)", path) + r"/?$"

    def _extract_params(self, path_regex, path):
        """
        Extracts parameters from the URL path based on the regex pattern.

        :param path_regex: The regex pattern of the path
        :param path: The URL path from the incoming request
        :return: A dictionary of extracted parameters
        """
        match = re.match(path_regex, path)
        return match.groupdict() if match else {}

    @staticmethod
    def normalize_path(path: str) -> str:
        """
        Normalizes the given path by removing multiple slashes and trailing slashes.
        This is useful for ensuring consistent path formatting.
        For example:
            - '/users//' becomes '/users'
            - '/users/:id/' becomes '/users/:id'
        and '/users/:id' remains unchanged.
        This function is particularly useful for ensuring that paths are in a consistent format
        before they are processed or stored.
        This function is also useful for ensuring that paths are in a consistent format

        Args:
            path (str): The path to be normalized.

        Returns:
            str: The normalized path.
        """
        # Collapse multiple slashes into one
        path = re.sub(r"\/+", "/", path)
        # Remove trailing slash unless it's root
        if path != "/" and path.endswith("/"):
            path = path[:-1]
        return path
