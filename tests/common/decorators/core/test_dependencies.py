from storm.common.constants import PARAMTYPES_METADATA
from storm.common.decorators.core.dependencies import Dependencies, flatten
from storm.core.di.reflect import Reflect


class Foo:
    pass


class Bar:
    pass


class Baz:
    pass


def test_flatten_single_level():
    assert flatten([1, 2, 3]) == [1, 2, 3]


def test_flatten_nested_lists():
    assert flatten([1, [2, [3, 4]], 5]) == [1, 2, 3, 4, 5]


def test_dependencies_stores_flat_list():
    @Dependencies(Foo, Bar)
    class ServiceA:
        pass

    metadata = Reflect.get_metadata(PARAMTYPES_METADATA, ServiceA)
    assert metadata == [Foo, Bar]


def test_dependencies_flattens_nested_lists():
    @Dependencies(Foo, [Bar, [Baz]])
    class ServiceB:
        pass

    metadata = Reflect.get_metadata(PARAMTYPES_METADATA, ServiceB)
    assert metadata == [Foo, Bar, Baz]
