import pytest
from storm.core.router import Router
from storm.core.router.request_handler import RequestHandler
class TestRouter:
    """Test cases for the Router and RequestHandler classes."""

    @pytest.fixture
    def router(self):
        """Fixture to create a Router instance for testing."""
        return Router()

    @pytest.mark.asyncio
    async def test_static_route(self, router):
        """Test that a static route is correctly resolved."""
        async def handler(params):
            return "static route"

        router.add_route('GET', '/static', handler)
        handler_func, params = router.resolve('GET', '/static')
        assert await handler_func(params) == "static route"

    @pytest.mark.asyncio
    async def test_dynamic_route(self, router):
        """Test that a dynamic route with parameters is correctly resolved."""
        async def handler(params):
            return f"user {params['id']}"

        router.add_route('GET', '/users/:id', handler)
        handler_func, params = router.resolve('GET', '/users/42')
        assert await handler_func(params) == "user 42"

    @pytest.mark.asyncio
    async def test_query_params(self, router):
        """Test that query parameters are correctly parsed and passed to the handler."""
        async def handler(params):
            return f"user {params['id']} with filter {params['filter'][0]}"

        router.add_route('GET', '/users/:id', handler)
        request_handler = RequestHandler(router)
        response, status_code = await request_handler.handle_request('GET', '/users/42', 'filter=active')
        assert response == "user 42 with filter active"
        assert status_code == 200

    @pytest.mark.asyncio
    async def test_route_not_found(self, router):
        """Test that a 404 error is returned when a route is not found."""
        request_handler = RequestHandler(router)
        response, status_code = await request_handler.handle_request('GET', '/nonexistent')
        assert status_code == 404
        assert response["error"] == "Route not found"
