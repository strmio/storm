import pytest
from storm.common.exceptions import (
    StormException, NotFoundException, UnauthorizedException,
    BadRequestException, ForbiddenException, ConflictException
)

def test_storm_exception():
    exception = StormException("Something went wrong", 500)
    assert exception.to_dict() == {"error": "Something went wrong", "status_code": 500}

def test_not_found_exception():
    exception = NotFoundException("Resource not found")
    assert exception.to_dict() == {"error": "Resource not found", "status_code": 404}

def test_unauthorized_exception():
    exception = UnauthorizedException("Unauthorized access")
    assert exception.to_dict() == {"error": "Unauthorized access", "status_code": 401}

def test_forbidden_exception():
    exception = ForbiddenException("Forbidden")
    assert exception.to_dict() == {"error": "Forbidden", "status_code": 403}

def test_conflict_exception():
    exception = ConflictException("Conflict")
    assert exception.to_dict() == {"error": "Conflict", "status_code": 409}
