import pytest

from storm.common.constants import MODULE_METADATA
from storm.common.decorators.modules.module import Module
from storm.core.di.reflect import Reflect


def test_module_decorator_sets_metadata():
    class Provider:
        pass

    class Controller:
        pass

    class ImportedModule:
        pass

    @Module(
        {
            "imports": [ImportedModule],
            "controllers": [Controller],
            "providers": [Provider],
            "exports": [Provider],
        }
    )
    class MyModule:
        pass

    assert Reflect.get_metadata(MODULE_METADATA["IMPORTS"], MyModule) == [ImportedModule]
    assert Reflect.get_metadata(MODULE_METADATA["CONTROLLERS"], MyModule) == [Controller]
    assert Reflect.get_metadata(MODULE_METADATA["PROVIDERS"], MyModule) == [Provider]
    assert Reflect.get_metadata(MODULE_METADATA["EXPORTS"], MyModule) == [Provider]


def test_module_decorator_raises_error_on_invalid_keys():
    with pytest.raises(ValueError) as exc_info:

        @Module({"invalidKey": []})
        class InvalidModule:
            pass

    assert "Invalid property 'invalidKey'" in str(exc_info.value)


def test_module_with_partial_metadata():
    class Controller:
        pass

    @Module(
        {
            "controllers": [Controller],
        }
    )
    class MyModule:
        pass

    assert Reflect.get_metadata(MODULE_METADATA["CONTROLLERS"], MyModule) == [Controller]
    assert Reflect.get_metadata(MODULE_METADATA["IMPORTS"], MyModule) is None
    assert Reflect.get_metadata(MODULE_METADATA["PROVIDERS"], MyModule) is None
    assert Reflect.get_metadata(MODULE_METADATA["EXPORTS"], MyModule) is None
