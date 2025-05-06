# tests/decorators/test_set_metadata.py

import pytest

from storm.common.decorators.core.set_metadata import SetMetadata
from storm.core.di.reflect import Reflect


@pytest.fixture(autouse=True)
def clear_reflect():
    Reflect.clear()


def test_set_metadata_on_class():
    @SetMetadata("role", "admin")
    class Admin:
        pass

    assert Reflect.get_metadata("role", Admin) == "admin"


def test_set_metadata_on_method():
    class Service:
        @SetMetadata("log", True)
        def act(self):
            pass

    assert Reflect.get_metadata("log", Service.act) is True


def test_set_metadata_exposes_key():
    dec = SetMetadata("key", "value")
    assert dec.KEY == "key"
