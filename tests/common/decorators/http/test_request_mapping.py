import pytest

from storm.common.constants import METHOD_METADATA, PATH_METADATA
from storm.common.decorators.http.request_mapping import (
    All,
    Copy,
    Delete,
    Get,
    Head,
    Lock,
    Mkcol,
    Move,
    Options,
    Patch,
    Post,
    Propfind,
    Proppatch,
    Put,
    Search,
    Unlock,
)
from storm.common.enums.request_method import RequestMethod
from storm.core.di.reflect import Reflect


@pytest.mark.parametrize(
    "decorator, method, path",
    [
        (Get("/get"), RequestMethod.GET, "/get"),
        (Get(), RequestMethod.GET, "/"),
        (Post("/post"), RequestMethod.POST, "/post"),
        (Put("/put"), RequestMethod.PUT, "/put"),
        (Delete("/delete"), RequestMethod.DELETE, "/delete"),
        (Patch("/patch"), RequestMethod.PATCH, "/patch"),
        (Options("/options"), RequestMethod.OPTIONS, "/options"),
        (Head("/head"), RequestMethod.HEAD, "/head"),
        (All("/all"), RequestMethod.ALL, "/all"),
        (Search("/search"), RequestMethod.SEARCH, "/search"),
        (Propfind("/propfind"), RequestMethod.PROPFIND, "/propfind"),
        (Proppatch("/proppatch"), RequestMethod.PROPPATCH, "/proppatch"),
        (Mkcol("/mkcol"), RequestMethod.MKCOL, "/mkcol"),
        (Copy("/copy"), RequestMethod.COPY, "/copy"),
        (Move("/move"), RequestMethod.MOVE, "/move"),
        (Lock("/lock"), RequestMethod.LOCK, "/lock"),
        (Unlock("/unlock"), RequestMethod.UNLOCK, "/unlock"),
    ],
)
def test_request_mapping_decorators(decorator, method, path):
    class TestController:
        @decorator
        def handler(self):
            pass

    metadata_path = Reflect.get_metadata(PATH_METADATA, TestController.handler)
    metadata_method = Reflect.get_metadata(METHOD_METADATA, TestController.handler)

    assert metadata_path == path
    assert metadata_method == method
