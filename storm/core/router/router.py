from collections import defaultdict
from typing import Optional
from storm.common.enums.versioning_type import VersioningType
from storm.common.services.logger import Logger
import re
from storm.core.adapters.http_request import HttpRequest
from storm.core.appliction_config import ApplicationConfig
from storm.core.interfaces.version_options_interface import VERSION_NEUTRAL


class Router:
    def __init__(self, app_config: ApplicationConfig | None = None):
        self.logger = Logger(self.__class__.__name__)
        self.app_config = app_config
        self.static_routes = defaultdict(
            lambda: defaultdict(dict)
        )  # method -> { path: handler }
        # method -> list of (specificity, path, regex, handler)
        self.dynamic_routes = defaultdict(lambda: defaultdict(list))
        # method -> { path: handler }
        self.sse_routes = defaultdict(lambda: defaultdict(dict))

    def add_sse_route(self, method, path, handler, version=None):
        """
        Registers a new SSE route with the specified HTTP method and path.
        """
        path = self.normalize_path(path)
        path_regex = self._path_to_regex(path)

        versions = (
            version if isinstance(version, list) else [version or VERSION_NEUTRAL]
        )

        for v in versions:
            if ":" in path:
                specificity = self._specificity(path)
                self.dynamic_routes[method][v].append(
                    (specificity, path, path_regex, handler)
                )
                self.dynamic_routes[method][v].sort(reverse=True)
            else:
                self.sse_routes[method][v][path] = handler

    def add_route(self, method, path, handler, version=None):
        """
        Registers a new route with the specified HTTP method and path.

        :param method: The HTTP method (GET, POST, etc.)
        :param path: The URL path (e.g., '/users/:id')
        :param handler: The function to handle requests to this route
        """
        path = self.normalize_path(path)
        path_regex = self._path_to_regex(path)

        versions = (
            version if isinstance(version, list) else [version or VERSION_NEUTRAL]
        )

        for v in versions:
            if ":" in path:
                specificity = self._specificity(path)
                self.dynamic_routes[method][v].append(
                    (specificity, path, path_regex, handler)
                )
                self.dynamic_routes[method][v].sort(reverse=True)
            else:
                self.static_routes[method][v][path] = handler

    def resolve(self, method, path, version=None, request=None):
        """
        Resolves a route for the given HTTP method, path, and version.

        If no route is found for the specific version, falls back to VERSION_NEUTRAL.
        """
        if request:
            version, path = self.extract_version(request)
        else:
            path = self.normalize_path(path)

        # Versions to try
        versions_to_try = [version or VERSION_NEUTRAL]

        if version is None and version != VERSION_NEUTRAL:
            versions_to_try.append(VERSION_NEUTRAL)

        for v in versions_to_try:
            # SSE static
            if path in self.sse_routes[method].get(v, {}):
                return self.sse_routes[method][v][path], {}

            # Normal static
            if path in self.static_routes[method].get(v, {}):
                return self.static_routes[method][v][path], {}

            # Normal dynamic
            for specificity, original_path, path_regex, handler in self.dynamic_routes[
                method
            ].get(v, []):
                match = path_regex.match(path)
                if match:
                    return handler, match.groupdict()

        raise ValueError(f"No route found for {method} {path} (version={version})")

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

    def extract_version(self, request: HttpRequest) -> tuple[Optional[str], str]:
        """
        Extracts the API version from the request according to the configured versioning strategy.
        Returns a tuple: (version, normalized_path)
        """
        versioning = self.app_config.get_versioning()
        if not self.app_config or not versioning:
            return None, self.normalize_path(request.path)

        path = request.path
        if versioning.type == VersioningType.URI:
            # Example: /v1/users
            prefix = versioning.prefix if versioning.prefix is not False else "v"
            match = re.match(rf"^/{prefix}(\d+)(/|$)", path)
            if match:
                version = match.group(1)
                # Remove /v1 from the path
                new_path = re.sub(rf"^/{prefix}{version}", "", path) or "/"
                return version, self.normalize_path(new_path)
            return None, self.normalize_path(path)

        elif versioning.type == VersioningType.HEADER:
            return request.get_header(versioning.header), self.normalize_path(path)

        elif versioning.type == VersioningType.MEDIA_TYPE:
            content_type = request.get_header("Content-Type", "")
            match = re.search(rf"{versioning.key}=([\w\d]+)", content_type)
            return (match.group(1) if match else None), self.normalize_path(path)

        elif versioning.type == VersioningType.CUSTOM:
            return versioning.extractor(request), self.normalize_path(path)

        return None, self.normalize_path(path)
