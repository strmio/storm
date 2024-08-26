# tests/test_global_interceptors.py

import pytest
from storm.core.application import StormApplication
from storm.core.global_interceptor import GlobalInterceptor
from storm.common.decorators.module import Module

class TestGlobalInterceptor(GlobalInterceptor):
    """
    Test interceptor that sets a flag in the request and modifies the response.
    """

    async def intercept(self, request, next_handler):
        request['interceptor_applied'] = True
        response = await next_handler(request)
        response += " intercepted"
        return response

@pytest.mark.asyncio
async def test_global_interceptor_execution():
    """
    Test to ensure that global interceptors are applied to the request and response.
    """

    @Module()
    class TestModule:
        pass

    app = StormApplication(root_module=TestModule)
    app.add_global_interceptor(TestGlobalInterceptor)

    async def test_handler(request):
        assert request.get('interceptor_applied') is True
        return "test passed"

    app.router.add_route('GET', '/test', test_handler)

    response, status_code = await app.handle_request('GET', '/test')
    assert response == "test passed intercepted"
    assert status_code == 200