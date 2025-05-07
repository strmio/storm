from storm.common.constants import GLOBAL_MODULE_METADATA
from storm.common.decorators.modules.global_decorator import Global
from storm.core.di.reflect import Reflect


def test_global_decorator_sets_metadata():
    @Global()
    class MyGlobalModule:
        pass

    assert Reflect.get_metadata(GLOBAL_MODULE_METADATA, MyGlobalModule) is True


def test_global_decorator_returns_class_unchanged():
    class Dummy:
        pass

    decorated = Global()(Dummy)
    assert decorated is Dummy
