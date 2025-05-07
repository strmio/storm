class ControllerDiscovery:
    def __init__(self, container, discovery_service):
        self.container = container
        self.discovery_service = discovery_service

    def discover_controllers(self, root_module):
        """
        Discover and register controllers in the root module.
        :param root_module: The root module containing the controllers.
        """
        controllers = []
        for controller in root_module.controllers:
            instance = self.container.resolve(controller.__class__.__name__)
            controllers.append(instance)
            self.discovery_service.register_service(controller.__class__.__name__, instance)
        return controllers
