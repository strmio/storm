from collections import defaultdict
from storm.common.services.logger import Logger
import re


class Router:
    def __init__(self):
        self.static_routes = defaultdict(dict)  # method -> { path: handler }
        self.dynamic_routes = defaultdict(
            list
        )  # method -> list of (specificity, path, regex, handler)
        self.sse_routes = defaultdict(dict)  # method -> { path: handler }
        self.logger = Logger(self.__class__.__name__)

    def add_sse_route(self, method, path, handler):
        """
        Registers a new SSE route with the specified HTTP method and path.
        """
        path = self.normalize_path(path)
        path_regex = self._path_to_regex(path)
        if ":" in path:
            specificity = self._specificity(path)
            self.dynamic_routes[method].append((specificity, path, path_regex, handler))
            self.dynamic_routes[method].sort(reverse=True)
        else:
            self.sse_routes[method][path] = handler

    def add_route(self, method, path, handler):
        """
        Registers a new route with the specified HTTP method and path.

        :param method: The HTTP method (GET, POST, etc.)
        :param path: The URL path (e.g., '/users/:id')
        :param handler: The function to handle requests to this route
        """
        path = self.normalize_path(path)
        path_regex = self._path_to_regex(path)
        if ":" in path:
            specificity = self._specificity(path)
            self.dynamic_routes[method].append((specificity, path, path_regex, handler))
            self.dynamic_routes[method].sort(reverse=True)
        else:
            self.static_routes[method][path] = handler

    def resolve(self, method, path):
        path = self.normalize_path(path)
        # Check SSE static routes
        if path in self.sse_routes[method]:
            return self.sse_routes[method][path], {}

        # Check normal static routes
        if path in self.static_routes[method]:
            return self.static_routes[method][path], {}

        # Check normal dynamic routes
        for specificity, original_path, path_regex, handler in self.dynamic_routes[
            method
        ]:
            match = path_regex.match(path)
            if match:
                return handler, match.groupdict()
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
        pattern = re.sub(r":(\w+)", r"(?P<\1>[^/]+)", path) + r"/?$"
        return re.compile(pattern)

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
