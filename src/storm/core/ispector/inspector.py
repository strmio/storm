class Inspector:
    def __init__(self, app):
        self.app = app

    def list_services(self):
        """
        List all registered services in the application.
        """
        print("Services:")
        for module in self.app.modules.values():
            for provider in module.providers:
                print(f" - {provider.__class__.__name__}")

    def list_controllers(self):
        """
        List all registered controllers in the application.
        """
        print("Controllers:")
        for module in self.app.modules.values():
            for controller in module.controllers:
                print(f" - {controller.__class__.__name__}")

    def list_routes(self):
        """
        List all registered routes in the application.
        """
        print("Routes:")
        for route in self.app.router.routes:
            print(f" - {route.method} {route.path} (Handler: {route.handler.__name__})")

    def inspect_service(self, service_name):
        """
        Inspect a specific service, showing its details.
        :param service_name: The name of the service to inspect.
        """
        service = next(
            (provider for module in self.app.modules.values()
             for provider in module.providers if provider.__class__.__name__ == service_name),
            None
        )
        if service:
            print(f"Service: {service.__class__.__name__}")
            print("Methods:")
            for method in dir(service):
                if callable(getattr(service, method)) and not method.startswith('_'):
                    print(f" - {method}")
        else:
            print(f"Service '{service_name}' not found.")