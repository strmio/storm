from storm.common.constants import VERSION_METADATA
from storm.common.decorators.core.version import Version
from storm.core.di.reflect import Reflect


def test_version_as_string():
    class Controller:
        @Version("1")
        def handler(self):
            pass

    func = Controller.__dict__["handler"]
    assert Reflect.get_metadata(VERSION_METADATA, func) == "1"


def test_version_as_list_with_duplicates():
    class Controller:
        @Version(["1", "2", "1"])
        def handler(self):
            pass

    func = Controller.__dict__["handler"]
    result = Reflect.get_metadata(VERSION_METADATA, func)
    assert result == ["1", "2"]
