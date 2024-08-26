# tests/test_global_middleware.py

import pytest
from storm.core.application import StormApplication
from storm.core.global_middleware import GlobalMiddleware
from storm.common.decorators.module import Module

class TestGlobalMiddleware(GlobalMiddleware):
    async def process(self, request, next_handler):
        request['global_middleware_applied'] = True
        return await next_handler(request)

@pytest.mark.asyncio
async def test_global_middleware_execution():
    @Module()
    class TestModule:
        pass

    app = StormApplication(root_module=TestModule)
    app.add_global_middleware(TestGlobalMiddleware)

    async def test_handler(request):
        assert request.get('global_middleware_applied') is True
        return "test passed"

    app.router.add_route('GET', '/test', test_handler)

    response, status_code = await app.handle_request('GET', '/test')
    assert response == "test passed"
    assert status_code == 200
