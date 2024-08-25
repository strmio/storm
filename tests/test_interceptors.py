import pytest
import asyncio
import logging
from storm.common.interceptors.logging_interceptor import LoggingInterceptor

@pytest.mark.asyncio
async def test_logging_interceptor(caplog):
    interceptor = LoggingInterceptor()

    # Simulate a request object
    class Request:
        def __init__(self, path):
            self.path = path

    request = Request(path="/example")

    with caplog.at_level(logging.INFO):
        # Use an asynchronous function for `next`
        async def next_function():
            return "Processed Response"
        
        response = await interceptor.intercept(request, next_function)
        
    assert "Request received: /example" in caplog.text
    assert "Response sent: Processed Response" in caplog.text
