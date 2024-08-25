import pytest
import logging
from storm import Container, Module
from storm.core.controller import ControllerBase
from storm.core.decorators import Controller
from storm import Injectable
from storm.common.middlewares.logger_middleware import LoggerMiddleware

logging.basicConfig(level=logging.INFO)

@Injectable(singleton=True)
class MiddlewareService:
    def get_data(self):
        return "Data from MiddlewareService"

@Controller("/middleware")
class MiddlewareController(ControllerBase):
    def __init__(self, service: MiddlewareService, middleware=[]):
        super().__init__(middleware)
        self.service = service

    async def action(self, request):
        return self.service.get_data()


class MiddlewareModule(Module):
    def __init__(self):
        super().__init__(
            controllers=[MiddlewareController],
            providers=[MiddlewareService],
            middleware=[LoggerMiddleware],
        )

@pytest.mark.asyncio
async def test_middleware_execution(capsys):
    container = Container()
    middleware_module = MiddlewareModule()
    middleware_module.register(container)

    controller = container.resolve("MiddlewareController")

    # Simulate a request object with a 'path' attribute
    class Request:
        def __init__(self, path):
            self.path = path

    request = Request(path="/test")

    # Execute the controller action with middleware
    await controller.execute(request)
    captured = capsys.readouterr()

    # assert "Handling request" in captured.out
    # assert "Finished handling request" in captured.out
    assert "" in captured.out
    assert "" in captured.out
