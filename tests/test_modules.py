import pytest
from storm.common.decorators.injectable import Injectable
from storm.common.decorators import Controller
from storm.core.container import Container
from storm.core.module import Module

# Service in a shared module
@Injectable(singleton=True)
class SharedService:
    def get_shared_data(self):
        return "Shared data from SharedService"

# Shared module
class SharedModule(Module):
    def __init__(self):
        super().__init__(
            providers=[SharedService],
        )

# Service in the main module
@Injectable(singleton=True)
class MainService:
    def __init__(self, shared_service: SharedService):
        self.shared_service = shared_service

    def get_data(self):
        return f"Main data with {self.shared_service.get_shared_data()}"

# Controller in the main module
@Controller("/main")
class MainController:
    def __init__(self, main_service: MainService):
        self.main_service = main_service

    def get(self):
        return self.main_service.get_data()

# Main application module
class AppModule(Module):
    def __init__(self):
        super().__init__(
            controllers=[MainController],
            providers=[MainService],
            imports=[SharedModule()],
        )

# Test the nested module architecture
def test_nested_modules():
    container = Container()
    app_module = AppModule()
    app_module.register(container)

    controller = container.resolve("MainController")
    assert controller.get() == "Main data with Shared data from SharedService"

def test_middleware():
    container = Container()
    app_module = AppModule()
    app_module.register(container)

    controller = container.resolve("MainController")
    response = controller.get()  # Assuming it's async, you might need `await controller.get()` in an async context
    assert response == "Main data with Shared data from SharedService"
    # Check the console output for middleware logs
