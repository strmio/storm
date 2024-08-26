import pytest
import logging
from storm.common.interceptors.caching_interceptor import CachingInterceptor
from storm.common.interceptors.error_handling_interceptor import ErrorHandlingInterceptor

@pytest.mark.asyncio
async def test_caching_interceptor():
    interceptor = CachingInterceptor()

    class Request:
        def __init__(self, path):
            self.path = path

    request = Request(path="/example")

    async def next_function():
        return "Processed Response"

    # First call should process and cache the result
    response = await interceptor.intercept(request, next_function)
    assert response == "Processed Response"

    # Second call should return cached result
    response = await interceptor.intercept(request, next_function)
    assert response == "Processed Response"

@pytest.mark.asyncio
async def test_error_handling_interceptor(caplog):
    interceptor = ErrorHandlingInterceptor()

    class Request:
        def __init__(self, path):
            self.path = path

    request = Request(path="/example")

    async def failing_function():
        raise Exception("Something went wrong")

    with caplog.at_level(logging.ERROR):
        response = await interceptor.intercept(request, failing_function)

    assert "An error occurred: Something went wrong" in caplog.text
    assert response == {"error": "Something went wrong"}
