import pytest
from storm.common.decorators.injectable import Injectable
from storm.common.decorators import Controller
from storm.core.container import Container
from storm.core.module import Module
@Injectable(singleton=True)
class ExampleService:
    def get_message(self):
        return "Hello from ExampleService"

@Controller("/example")
class ExampleController:
    def __init__(self, service: ExampleService):
        self.service = service

    def get(self):
        return self.service.get_message()

class ExampleModule(Module):
    def __init__(self):
        super().__init__(
            controllers=[ExampleController],
            providers=[ExampleService],
        )

def test_service_injection():
    container = Container()
    example_module = ExampleModule()
    example_module.register(container)

    controller = container.resolve("ExampleController")
    assert controller.get() == "Hello from ExampleService"
