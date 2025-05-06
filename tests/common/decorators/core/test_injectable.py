# tests/decorators/test_injectable.py

import pytest

from storm.common.constants import INJECTABLE_WATERMARK, SCOPE_OPTIONS_METADATA
from storm.common.decorators.core.injectable import Injectable, Mixin
from storm.common.interfaces.scope_options import Scope
from storm.core.di.reflect import Reflect


@pytest.fixture(autouse=True)
def reset_reflect():
    Reflect.clear()


def test_injectable_default_scope():
    @Injectable()
    class MyService:
        pass

    assert Reflect.get_metadata(INJECTABLE_WATERMARK, MyService) is True
    assert Reflect.get_metadata(SCOPE_OPTIONS_METADATA, MyService) is None


def test_injectable_with_scope_and_durable():
    @Injectable(scope=Scope.REQUEST, durable=True)
    class MyScopedService:
        pass

    metadata = Reflect.get_metadata(SCOPE_OPTIONS_METADATA, MyScopedService)
    assert metadata == {"scope": Scope.REQUEST, "durable": True}


def test_mixin_generates_unique_name_and_is_injectable():
    class DynamicService:
        pass

    mixed = Mixin(DynamicService)
    assert mixed.__name__.startswith("Mixin_")
    assert Reflect.get_metadata(INJECTABLE_WATERMARK, mixed) is True


def test_injectable_with_only_durable():
    @Injectable(durable=True)
    class DurableService:
        pass

    metadata = Reflect.get_metadata(SCOPE_OPTIONS_METADATA, DurableService)
    assert metadata == {"scope": None, "durable": True}


def test_injectable_with_transient_scope():
    @Injectable(scope=Scope.TRANSIENT)
    class TransientService:
        pass

    metadata = Reflect.get_metadata(SCOPE_OPTIONS_METADATA, TransientService)
    assert metadata == {"scope": Scope.TRANSIENT, "durable": None}


def test_injectable_metadata_is_not_inherited_by_subclass():
    @Injectable(scope=Scope.DEFAULT)
    class BaseService:
        pass

    class ChildService(BaseService):
        pass

    # Subclases no deben heredar automáticamente metadatos del padre
    assert Reflect.get_metadata(SCOPE_OPTIONS_METADATA, ChildService) is None
    assert Reflect.get_metadata(INJECTABLE_WATERMARK, ChildService) is None


def test_mixin_multiple_calls_generate_unique_names():
    class Raw:
        pass

    mixin1 = Mixin(Raw)
    mixin2 = Mixin(type("Another", (), {}))

    assert mixin1.__name__ != mixin2.__name__
    assert Reflect.get_metadata(INJECTABLE_WATERMARK, mixin1) is True
    assert Reflect.get_metadata(INJECTABLE_WATERMARK, mixin2) is True
