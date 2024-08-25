import pytest
import asyncio
from storm.common.guards.role_guard import RoleGuard

@pytest.mark.asyncio
async def test_role_guard():
    guard = RoleGuard(allowed_roles=["admin", "user"])

    # Test with an allowed role
    class Request:
        def __init__(self, role):
            self.role = role

    request = Request(role="admin")
    result = await guard.can_activate(request)
    assert result == True

    # Test with a disallowed role
    request = Request(role="guest")
    result = await guard.can_activate(request)
    assert result == False
