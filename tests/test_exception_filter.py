import pytest
from storm.common.exceptions import NotFoundException, StormException
from storm.core.filter import ExceptionFilter

@pytest.mark.asyncio
async def test_exception_filter_handles_known_exceptions():
    exception = NotFoundException("Not found")
    response, status_code = await ExceptionFilter.handle_exception(exception)
    assert response == {"error": "Not found", "status_code": 404}
    assert status_code == 404

@pytest.mark.asyncio
async def test_exception_filter_handles_unknown_exceptions():
    exception = Exception("Unknown error")
    response, status_code = await ExceptionFilter.handle_exception(exception)
    assert response == {"error": "Internal server error", "status_code": 500}
    assert status_code == 500
