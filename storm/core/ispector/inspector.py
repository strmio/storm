from storm.common.services.logger import Logger


class Inspector:
    def __init__(self, app):
        self.logger = Logger(self.__class__.__name__)
        self.app = app

    def list_services(self):
        """
        List all registered services in the application.
        """
        self.logger.info("Services:")
        for module in self.app.modules.values():
            for provider in module.providers:
                self.logger.info(f" - {provider.__class__.__name__}")

    def list_controllers(self):
        """
        List all registered controllers in the application.
        """
        self.logger.info("Controllers:")
        for module in self.app.modules.values():
            for controller in module.controllers:
                self.logger.info(f" - {controller.__class__.__name__}")

    def list_routes(self):
        """
        List all registered routes in the application.
        """
        self.logger.info("Routes:")
        for route in self.app.router.routes:
            self.logger.info(f" - {route.method} {route.path} (Handler: {route.handler.__name__})")

    def inspect_service(self, service_name):
        """
        Inspect a specific service, showing its details.
        :param service_name: The name of the service to inspect.
        """
        service = next(
            (
                provider
                for module in self.app.modules.values()
                for provider in module.providers
                if provider.__class__.__name__ == service_name
            ),
            None,
        )
        if service:
            self.logger.info(f"Service: {service.__class__.__name__}")
            self.logger.info("Methods:")
            for method in dir(service):
                if callable(getattr(service, method)) and not method.startswith("_"):
                    self.logger.info(f" - {method}")
        else:
            self.logger.info(f"Service '{service_name}' not found.")
