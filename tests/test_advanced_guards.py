import pytest
import asyncio
from datetime import datetime

from storm.common.guards.time_based_guard import TimeBasedGuard

@pytest.mark.asyncio
async def test_time_based_guard():
    # Custom time provider to simulate the current time
    def mock_now():
        return datetime(2024, 1, 1, 10, 0)  # 10:00 AM

    guard = TimeBasedGuard(start_hour=9, end_hour=17, time_provider=mock_now)

    class Request:
        def __init__(self):
            pass

    request = Request()
    result = await guard.can_activate(request)
    assert result == True

    # Custom time provider to simulate time outside of allowed hours
    def mock_now_outside_hours():
        return datetime(2024, 1, 1, 8, 0)  # 8:00 AM

    guard = TimeBasedGuard(start_hour=9, end_hour=17, time_provider=mock_now_outside_hours)
    result = await guard.can_activate(request)
    assert result == False
