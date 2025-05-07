from storm.common.execution_context import ExecutionContext


def _wrap_sse_handler(handler):
    """
    Wraps an SSE (Server-Sent Events) handler to adapt it for sending SSE events.

    :param handler: An asynchronous function that returns an asynchronous generator.
                    The generator yields data to be sent as SSE events.
    :return: An asynchronous function that handles the SSE communication lifecycle,
             including sending headers, streaming events, and closing the connection.
    """

    async def sse_adapter(*args, **kwargs):
        request = ExecutionContext.get_request()
        response = ExecutionContext.get_response()
        if request is None:
            raise ValueError("Request object is missing")
        if response is None:
            raise ValueError("Response object is missing")

        await response.send_sse_headers(request.send)

        try:
            generator = await handler()
            async for data in generator:
                await response.send_sse_event(
                    request.send,
                    data=data,
                )
        finally:
            await response.close_sse(request.send)

    return sse_adapter
