import pytest
from storm.core.application import StormApplication
from storm.common.decorators.module import Module

@pytest.mark.asyncio
async def test_storm_application():
    @Module()
    class TestModule:
        pass

    app = StormApplication(root_module=TestModule)

    # Define the route handler function to accept the request argument
    async def test_handler(request):
        return "test passed"

    # Add the route using the app's router
    app.router.add_route('GET', '/test', test_handler)

    # Handle a request and assert the response
    response, status_code = await app.handle_request('GET', '/test')
    assert response == "test passed"
    assert status_code == 200
