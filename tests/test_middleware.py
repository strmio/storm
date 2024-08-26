import pytest
import logging
from storm import Container, Module
from storm.core.controller import ControllerBase
from storm.core.decorators import Controller
from storm import Injectable
from storm.common.middlewares.logger_middleware import LoggerMiddleware
from storm.core.middleware import Middleware
from storm.core.middleware_pipeline import MiddlewarePipeline

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

class TestMiddleware(Middleware):
    async def process_request(self, request, next_handler):
        request['processed'] = True
        return await next_handler(request)

    async def process_response(self, response):
        response['middleware'] = "processed"
        return response

@pytest.mark.asyncio
async def test_middleware_pipeline():
    pipeline = MiddlewarePipeline([TestMiddleware()])
    
    async def final_handler(request):
        return {"response": "final"}

    request = {}
    response = await pipeline.execute(request, final_handler)
    # assert response['middleware'] == "processed"
    assert request['processed'] is True
