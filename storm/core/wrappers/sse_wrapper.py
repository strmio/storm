from storm.common.execution_context import execution_context


def _wrap_sse_handler(handler):
    async def sse_adapter(*args, **kwargs):
        request = execution_context.get_request()
        response = execution_context.get_response()

        await response.send_sse_headers(request.send)

        try:
            generator = await handler()
            async for event in generator:
                await response.send_sse_event(
                    request.send,
                    data=event.get("data"),
                    event=event.get("event"),
                    id=event.get("id"),
                )
        finally:
            await response.close_sse(request.send)

    return sse_adapter
