class Container:
    def __init__(self):
        self.services = {}

    def register(self, name, service):
        self.services[name] = service

    def resolve(self, name):
        service = self.services.get(name)
        if not service:
            raise Exception(f"Service {name} not found.")
        return service
