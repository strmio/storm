# tests/test_decorators.py

import pytest
from storm.common.decorators.http import route, get, post, routes

@pytest.mark.asyncio
async def test_route_decorator():
    @route('GET', '/test')
    async def test_handler():
        return "test passed"

    handler, _ = routes.resolve('GET', '/test')
    response = await handler()
    assert response == "test passed"

@pytest.mark.asyncio
async def test_http_method_decorators():
    @get('/test-get')
    async def test_get_handler():
        return "GET passed"

    @post('/test-post')
    async def test_post_handler():
        return "POST passed"

    handler, _ = routes.resolve('GET', '/test-get')
    response = await handler()
    assert response == "GET passed"

    handler, _ = routes.resolve('POST', '/test-post')
    response = await handler()
    assert response == "POST passed"
