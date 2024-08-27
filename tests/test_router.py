import pytest
from storm.core.router import Router

@pytest.mark.asyncio
async def test_router_add_and_resolve_route():
    router = Router()

    async def handler(id):
        return f"Handled {id}"

    router.add_route('GET', '/test/:id', handler)  # Properly add the route with a defined handler

    resolved_handler, params = router.resolve('GET', '/test/123')
    assert resolved_handler == handler
    assert params == {'id': '123'}

    response = await resolved_handler(**params)
    assert response == "Handled 123"
