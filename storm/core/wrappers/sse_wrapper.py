from storm.common.execution_context import execution_context


def _wrap_sse_handler(handler):
    """
    Wraps an SSE (Server-Sent Events) handler to adapt it for sending SSE events.

    :param handler: An asynchronous function that returns an asynchronous generator.
                    The generator yields data to be sent as SSE events.
    :return: An asynchronous function that handles the SSE communication lifecycle,
             including sending headers, streaming events, and closing the connection.
    """
    async def sse_adapter(*args, **kwargs):
        request = execution_context.get_request()
        response = execution_context.get_response()

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
