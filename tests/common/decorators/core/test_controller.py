import pytest

from storm.common.constants import CONTROLLER_WATERMARK, HOST_METADATA, PATH_METADATA, SCOPE_OPTIONS_METADATA, VERSION_METADATA
from storm.common.decorators.core.controller import Controller, ControllerOptions
from storm.common.interfaces.scope_options import Scope
from storm.core.di.reflect import Reflect
from storm.core.interfaces.version_options_interface import VERSION_NEUTRAL


@pytest.fixture(autouse=True)
def clear_reflect():
    Reflect.clear()


def test_controller_without_args():
    @Controller()
    class TestController:
        pass

    assert Reflect.get_metadata(CONTROLLER_WATERMARK, TestController) is True
    assert Reflect.get_metadata(PATH_METADATA, TestController) == "/"
    assert Reflect.get_metadata(HOST_METADATA, TestController) is None
    assert Reflect.get_metadata(SCOPE_OPTIONS_METADATA, TestController) is None
    assert Reflect.get_metadata(VERSION_METADATA, TestController) is None


def test_controller_with_path_string():
    @Controller("/users")
    class TestController:
        pass

    assert Reflect.get_metadata(PATH_METADATA, TestController) == "/users"


def test_controller_with_path_list():
    @Controller(["/users", "/clients"])
    class TestController:
        pass

    assert Reflect.get_metadata(PATH_METADATA, TestController) == ["/users", "/clients"]


def test_controller_with_options():
    options = ControllerOptions(path="/api", host="example.com", scope=Scope.REQUEST, durable=True, version="1.0")

    @Controller(options)
    class TestController:
        pass

    assert Reflect.get_metadata(CONTROLLER_WATERMARK, TestController) is True
    assert Reflect.get_metadata(PATH_METADATA, TestController) == "/api"
    assert Reflect.get_metadata(HOST_METADATA, TestController) == "example.com"
    assert Reflect.get_metadata(SCOPE_OPTIONS_METADATA, TestController) == {
        "scope": Scope.REQUEST,
        "durable": True,
    }
    assert Reflect.get_metadata(VERSION_METADATA, TestController) == "1.0"


def test_controller_with_neutral_version():
    options = ControllerOptions(version=VERSION_NEUTRAL)

    @Controller(options)
    class TestController:
        pass

    assert Reflect.get_metadata(VERSION_METADATA, TestController) is VERSION_NEUTRAL


def test_controller_invalid_argument_raises_type_error():
    with pytest.raises(TypeError):

        @Controller(123)  # invalid type
        class InvalidController:
            pass


def test_controller_with_empty_path_list_defaults_to_root():
    @Controller([])
    class TestController:
        pass

    assert Reflect.get_metadata(PATH_METADATA, TestController) == []


def test_multiple_controllers_dont_share_metadata():
    @Controller("/a")
    class A:
        pass

    @Controller("/b")
    class B:
        pass

    assert Reflect.get_metadata(PATH_METADATA, A) == "/a"
    assert Reflect.get_metadata(PATH_METADATA, B) == "/b"


def test_controller_with_none_options_defaults_to_root():
    @Controller(None)
    class TestController:
        pass

    assert Reflect.get_metadata(PATH_METADATA, TestController) == "/"


def test_controller_with_partial_options():
    options = ControllerOptions(path="/partial", version=["1", "2"])

    @Controller(options)
    class TestController:
        pass

    assert Reflect.get_metadata(PATH_METADATA, TestController) == "/partial"
    assert Reflect.get_metadata(VERSION_METADATA, TestController) == ["1", "2"]


def test_controller_with_duplicate_versions_removes_duplicates():
    options = ControllerOptions(version=["1", "1", "2", "2"])

    @Controller(options)
    class TestController:
        pass

    assert sorted(Reflect.get_metadata(VERSION_METADATA, TestController)) == ["1", "2"]


def test_controller_inheritance_metadata_not_inherited_by_default():
    @Controller("/base")
    class Base:
        pass

    class Derived(Base):
        pass

    # Inheriting class won't get metadata unless explicitly decorated
    assert Reflect.get_metadata(PATH_METADATA, Derived) is None
    assert Reflect.get_metadata(PATH_METADATA, Base) == "/base"
