# tests/common/decorators/http/test_sse.py

from storm.common.constants import METHOD_METADATA, PATH_METADATA, SSE_METADATA
from storm.common.decorators.http.sse import Sse
from storm.common.enums.request_method import RequestMethod
from storm.core.di.reflect import Reflect


def test_sse_decorator_sets_correct_metadata():
    @Sse("/events")
    def handle_sse():
        pass

    assert Reflect.get_metadata(PATH_METADATA, handle_sse) == "/events"
    assert Reflect.get_metadata(METHOD_METADATA, handle_sse) == RequestMethod.GET
    assert Reflect.get_metadata(SSE_METADATA, handle_sse) is True


def test_sse_defaults_to_root_path():
    @Sse()
    def default_sse():
        pass

    assert Reflect.get_metadata(PATH_METADATA, default_sse) == "/"
