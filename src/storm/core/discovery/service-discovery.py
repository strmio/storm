
class DiscoveryService:
    def __init__(self):
        self._registry = {}

    def register_service(self, service_name, service_instance):
        """
        Register a service in the discovery registry.
        :param service_name: The name of the service to register.
        :param service_instance: The instance of the service to register.
        """
        self._registry[service_name] = service_instance
        print(f"Service '{service_name}' registered successfully.")

    def get_service(self, service_name):
        """
        Retrieves a service by its name from the discovery registry.
        :param service_name: The name of the service to retrieve.
        :return: The service instance, or None if not found.
        """
        service = self._registry.get(service_name)
        if service:
            print(f"Service '{service_name}' found.")
            return service
        else:
            print(f"Service '{service_name}' not found.")
            return None

    def list_services(self):
        """
        Lists all registered services in the discovery registry.
        """
        print("Registered Services:")
        for service_name in self._registry:
            print(f" - {service_name}")
