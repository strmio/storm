from storm.common.constants import (
    PARAMTYPES_METADATA,
    PROPERTY_DEPS_METADATA,
    SELF_DECLARED_DEPS_METADATA,
)
from storm.common.decorators.core.inject import Inject
from storm.core.di.reflect import Reflect


def test_inject_decorator_on_constructor_parameter_with_token():
    class Token:
        pass

    class Service:
        def __init__(self, dep):
            pass

    Inject(Token)(Service.__init__, None, 0)

    metadata = Reflect.get_metadata(SELF_DECLARED_DEPS_METADATA, Service.__init__)
    assert metadata == [{"index": 0, "param": Token}]


def test_inject_decorator_on_constructor_parameter_without_token_infers_type():
    class Token:
        pass

    class Service:
        def __init__(self, dep):
            pass

    Reflect.define_metadata(PARAMTYPES_METADATA, [Token], Service.__init__)
    Inject()(Service.__init__, None, 0)

    metadata = Reflect.get_metadata(SELF_DECLARED_DEPS_METADATA, Service.__init__)
    assert metadata == [{"index": 0, "param": Token}]


def test_inject_decorator_on_property_with_token():
    class Token:
        pass

    class Service:
        my_dep = None

    Inject(Token)(Service, "my_dep")

    metadata = Reflect.get_metadata(PROPERTY_DEPS_METADATA, Service)
    assert metadata == [{"key": "my_dep", "type": Token}]


def test_inject_infers_property_type_from_design_metadata():
    class Foo:
        pass

    class Service:
        my_prop = None

    Reflect.define_metadata("design:type", Foo, Service, "my_prop")
    Inject()(Service, "my_prop")

    metadata = Reflect.get_metadata(PROPERTY_DEPS_METADATA, Service)
    assert metadata == [{"key": "my_prop", "type": Foo}]
