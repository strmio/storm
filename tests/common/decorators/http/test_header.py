from storm.common.constants import HEADERS_METADATA
from storm.common.decorators.http.header import Header
from storm.core.di.reflect import Reflect


def test_header_decorator_sets_static_value():
    class MyController:
        @Header("Cache-Control", "no-store")
        def handler(self):
            pass

    metadata = Reflect.get_metadata(HEADERS_METADATA, MyController.handler)
    assert metadata == [{"name": "Cache-Control", "value": "no-store"}]


def test_header_decorator_sets_dynamic_value():
    class MyController:
        @Header("Cache-Control", lambda: "private")
        def handler(self):
            pass

    metadata = Reflect.get_metadata(HEADERS_METADATA, MyController.handler)
    assert len(metadata) == 1
    assert metadata[0]["name"] == "Cache-Control"
    assert callable(metadata[0]["value"])
    assert metadata[0]["value"]() == "private"


def test_header_decorator_appends_multiple_headers():
    class MyController:
        @Header("Cache-Control", "no-cache")
        @Header("X-Custom-Header", "abc123")
        def handler(self):
            pass

    metadata = Reflect.get_metadata(HEADERS_METADATA, MyController.handler)
    assert metadata == [
        {"name": "X-Custom-Header", "value": "abc123"},
        {"name": "Cache-Control", "value": "no-cache"},
    ]
