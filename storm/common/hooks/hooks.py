from abc import ABC, abstractmethod


class OnModuleInit(ABC):
    @abstractmethod
    def on_module_init(self):
        """Called after the module has been initialized."""
        pass


class OnApplicationBootstrap(ABC):
    @abstractmethod
    def on_application_bootstrap(self):
        """Called after the application has fully bootstrapped."""
        pass


class OnApplicationShutdown(ABC):
    @abstractmethod
    def on_application_shutdown(self, signal: str):
        """Called during application shutdown."""
        pass
