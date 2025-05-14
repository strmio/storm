from typing import Any

from storm.common.constants import ROUTE_ARGS_METADATA
from storm.common.decorators.http.route_params import (
    Body,
    Headers,
    HostParam,
    Ip,
    Next,
    Param,
    Query,
    RawBody,
    Request,
    Response,
    Session,
    UploadedFile,
    UploadedFiles,
    register_param_metadata,
)
from storm.common.enums.request_param_type import RouteParamtypes
from storm.common.interfaces.features.pipe_transform import PipeTransform
from storm.core.di.reflect import Reflect


class DummyPipe(PipeTransform):
    def transform(self, value: Any, metadata: Any = None) -> Any:
        return value


def get_metadata(cls, method_name):
    return Reflect.get_metadata(ROUTE_ARGS_METADATA, cls, method_name)


def test_param_marker():
    class Controller:
        def handler(self, user_id=Param("id", DummyPipe())):
            pass

    register_param_metadata(Controller, "handler")
    metadata = get_metadata(Controller, "handler")
    assert metadata[f"{RouteParamtypes.PARAM}:0"]["data"] == "id"
    assert isinstance(metadata[f"{RouteParamtypes.PARAM}:0"]["pipes"][0], DummyPipe)


def test_query_marker():
    class Controller:
        def handler(self, lang=Query("lang")):
            pass

    register_param_metadata(Controller, "handler")
    metadata = get_metadata(Controller, "handler")
    assert metadata[f"{RouteParamtypes.QUERY}:0"]["data"] == "lang"


def test_body_marker():
    class Controller:
        def handler(self, payload=Body("user")):
            pass

    register_param_metadata(Controller, "handler")
    metadata = get_metadata(Controller, "handler")
    assert metadata[f"{RouteParamtypes.BODY}:0"]["data"] == "user"


def test_headers_marker():
    class Controller:
        def handler(self, auth=Headers("authorization")):
            pass

    register_param_metadata(Controller, "handler")
    metadata = get_metadata(Controller, "handler")
    assert metadata[f"{RouteParamtypes.HEADERS}:0"]["data"] == "authorization"


def test_uploaded_file_marker():
    class Controller:
        def handler(self, upload=UploadedFile("doc")):
            pass

    register_param_metadata(Controller, "handler")
    metadata = get_metadata(Controller, "handler")
    assert metadata[f"{RouteParamtypes.FILE}:0"]["data"] == "doc"


def test_uploaded_files_marker():
    class Controller:
        def handler(self, uploads=UploadedFiles(DummyPipe())):
            pass

    register_param_metadata(Controller, "handler")
    metadata = get_metadata(Controller, "handler")
    assert isinstance(metadata[f"{RouteParamtypes.FILES}:0"]["pipes"][0], DummyPipe)


def test_raw_body_marker():
    class Controller:
        def handler(self, raw=RawBody(DummyPipe())):
            pass

    register_param_metadata(Controller, "handler")
    metadata = get_metadata(Controller, "handler")
    assert isinstance(metadata[f"{RouteParamtypes.RAW_BODY}:0"]["pipes"][0], DummyPipe)


def test_special_markers():
    class Controller:
        def handler(self, ip=Ip(), session=Session(), req=Request(), res=Response(), next_=Next(), host=HostParam("sub")):
            pass

    register_param_metadata(Controller, "handler")
    metadata = get_metadata(Controller, "handler")
    assert metadata[f"{RouteParamtypes.IP}:0"]["data"] is None
    assert metadata[f"{RouteParamtypes.SESSION}:1"]["data"] is None
    assert metadata[f"{RouteParamtypes.REQUEST}:2"]["data"] is None
    assert metadata[f"{RouteParamtypes.RESPONSE}:3"]["data"] is None
    assert metadata[f"{RouteParamtypes.NEXT}:4"]["data"] is None
    assert metadata[f"{RouteParamtypes.HOST}:5"]["data"] == "sub"


def test_no_route_param_markers():
    class Controller:
        def handler(self, a: int, b: str):
            pass

    register_param_metadata(Controller, "handler")
    metadata = get_metadata(Controller, "handler")
    assert metadata == {}
