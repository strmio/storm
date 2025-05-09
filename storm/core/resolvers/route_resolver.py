from storm.common.services.logger import Logger
from storm.core.router.router import Router
from storm.core.wrappers.sse_wrapper import _wrap_sse_handler


class RouteExplorer:
    """
    Resolves and validates routes for controllers and their methods.
    """

    def __init__(self):
        self.logger = Logger(self.__class__.__name__)

    def explore_route(self, controller, attr_name: str, base_path: str):
        """
        Resolve a route from the given controller method.

        :param controller: The controller instance containing the route method.
        :param attr_name: The name of the method on the controller.
        :param base_path: The base path for the controller.
        :return: A dictionary with the route information or None if not a valid route.
        """
        attr = getattr(controller, attr_name)
        if callable(attr) and hasattr(attr, "_route"):
            attr = getattr(controller, attr_name)
            if callable(attr) and hasattr(attr, "_route"):
                normalization_path = Router.normalize_path(base_path + attr._route["path"])
                if attr._route.get("version"):
                    self.logger.info(f"Mapped: {{{normalization_path}, {attr._route['method']}}} (version: {attr._route['version']}) route")
                else:
                    self.logger.info(f"Mapped: {{{normalization_path}, {attr._route['method']}}} route")
                route_info = {
                    # HTTP method (e.g., GET, POST)
                    "method": attr._route["method"],
                    "path": normalization_path,  # Full route path
                    "handler": attr,  # The handler method
                    "is_sse": getattr(attr, "is_sse", False),
                    "version": attr._route.get("version"),
                }
                return route_info
        return None


class RouteResolver:
    """
    Explores and stores routes for the application.
    """

    def __init__(self, router: Router):
        """
        Initialize the RouteExplorer.

        :param router: The application's Router instance.
        """
        self.logger = Logger(self.__class__.__name__)
        self.router = router

    def register_routes(self, controller, base_path: str, explorer: RouteExplorer):
        """
        Explore and register routes from a controller using the RouteResolver.

        :param controller: The controller instance to explore.
        :param base_path: The base path for the controller.
        :param resolver: An instance of RouteResolver to resolve routes.
        """
        normilized_prefix = self.router.get_prefix() or ""
        normilized_path = self.router.normalize_path(base_path)
        path = normilized_prefix + normilized_path
        self.logger.info(f"{controller.__class__.__name__} {{{Router.normalize_path(path)}}}")

        for attr_name in dir(controller):
            route_info = explorer.explore_route(controller, attr_name, path)
            if route_info:
                version = route_info.get("version")

                if route_info.get("is_sse"):
                    sse_handler = _wrap_sse_handler(route_info["handler"])
                    self.router.add_sse_route(route_info["method"], route_info["path"], sse_handler, version)
                else:
                    self.router.add_route(
                        route_info["method"],
                        route_info["path"],
                        route_info["handler"],
                        version,
                    )
