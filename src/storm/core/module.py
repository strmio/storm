class Module:
    def __init__(self, controllers=[], providers=[]):
        self.controllers = controllers
        self.providers = providers

    def register(self, container):
        for provider in self.providers:
            container.register(provider.__name__, provider)
