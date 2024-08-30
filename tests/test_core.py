import pytest

from storm.common.decorators.injectable import Injectable
from storm.common.decorators import Controller
from storm.core.container import Container
from storm.core.module import ModuleBase


@Injectable(singleton=True)
class ExampleService:
    def get_data(self):
        return "This is some data from the service."


@Controller("/example")
class ExampleController:
    def __init__(self, service: ExampleService):
        self.service = service

    def get(self):
        return self.service.get_data()


class ExampleModule(ModuleBase):
    def __init__(self):
        super().__init__(
            controllers=[ExampleController],
            providers=[ExampleService],
        )


def test_dependency_injection():
    container = Container()
    module = ExampleModule()
    module.register(container)

    controller = container.resolve("ExampleController")
    assert controller.get() == "This is some data from the service."
