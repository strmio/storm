# test_reflect.py
import pytest

from storm.core.di.reflect import Reflect


@pytest.fixture(autouse=True)
def clear_reflect():
    Reflect.clear()


class MyClass:
    pass


class Example:
    pass


class Another:
    pass


class MyOtherClass:
    pass


def test_define_and_get_class_metadata():
    Reflect.define_metadata("meta:role", "admin", MyClass)
    assert Reflect.get_metadata("meta:role", MyClass) == "admin"


def test_has_metadata():
    Reflect.define_metadata("meta:permission", "read", MyClass)
    assert Reflect.has_metadata("meta:permission", MyClass)
    assert not Reflect.has_metadata("meta:permission", MyOtherClass)


def test_get_metadata_keys():
    Reflect.define_metadata("meta:1", "one", MyClass)
    Reflect.define_metadata("meta:2", "two", MyClass)
    keys = Reflect.get_metadata_keys(MyClass)
    assert set(keys) == {"meta:1", "meta:2"}


def test_delete_metadata():
    Reflect.define_metadata("meta:temp", "value", MyClass)
    deleted = Reflect.delete_metadata("meta:temp", MyClass)
    assert deleted is True
    assert not Reflect.has_metadata("meta:temp", MyClass)


def test_property_metadata():
    Reflect.define_metadata("meta:info", 123, MyClass, "prop")
    assert Reflect.has_metadata("meta:info", MyClass, "prop")
    assert Reflect.get_metadata("meta:info", MyClass, "prop") == 123
    keys = Reflect.get_metadata_keys(MyClass, "prop")
    assert keys == ["meta:info"]
    Reflect.delete_metadata("meta:info", MyClass, "prop")
    assert not Reflect.has_metadata("meta:info", MyClass, "prop")


def test_metadata_is_isolated_per_target():
    Reflect.define_metadata("meta:type", "int", MyClass)
    Reflect.define_metadata("meta:type", "str", MyOtherClass)
    assert Reflect.get_metadata("meta:type", MyClass) == "int"
    assert Reflect.get_metadata("meta:type", MyOtherClass) == "str"


def test_define_metadata_multiple_keys_same_property():
    Reflect.define_metadata("key1", "val1", Example, "prop")
    Reflect.define_metadata("key2", "val2", Example, "prop")
    assert Reflect.get_metadata("key1", Example, "prop") == "val1"
    assert Reflect.get_metadata("key2", Example, "prop") == "val2"
    keys = Reflect.get_metadata_keys(Example, "prop")
    assert set(keys) == {"key1", "key2"}


def test_define_metadata_overwrites_existing_key():
    Reflect.define_metadata("key", "old", Example)
    Reflect.define_metadata("key", "new", Example)
    assert Reflect.get_metadata("key", Example) == "new"
    keys = Reflect.get_metadata_keys(Example)
    assert keys == ["key"]


def test_delete_nonexistent_metadata_returns_false():
    assert not Reflect.delete_metadata("nonexistent", Example)
    Reflect.define_metadata("exists", 1, Example)
    Reflect.delete_metadata("exists", Example)
    assert not Reflect.delete_metadata("exists", Example)


def test_isolated_metadata_for_properties_and_class():
    Reflect.define_metadata("k", "class", Example)
    Reflect.define_metadata("k", "prop", Example, "x")
    assert Reflect.get_metadata("k", Example) == "class"
    assert Reflect.get_metadata("k", Example, "x") == "prop"
    assert Reflect.get_metadata_keys(Example) == ["k"]
    assert Reflect.get_metadata_keys(Example, "x") == ["k"]


def test_different_classes_same_key():
    Reflect.define_metadata("k", "one", Example)
    Reflect.define_metadata("k", "two", Another)
    assert Reflect.get_metadata("k", Example) == "one"
    assert Reflect.get_metadata("k", Another) == "two"


def test_get_metadata_returns_none_if_not_exists():
    assert Reflect.get_metadata("missing", Example) is None


def test_delete_metadata_on_property():
    Reflect.define_metadata("key", "value", Example, "foo")
    assert Reflect.delete_metadata("key", Example, "foo")
    assert not Reflect.has_metadata("key", Example, "foo")
    assert Reflect.get_metadata("key", Example, "foo") is None


def test_property_key_accepts_int():
    Reflect.define_metadata("intkey", 100, Example, 42)
    assert Reflect.get_metadata("intkey", Example, 42) == 100
    assert Reflect.has_metadata("intkey", Example, 42)
