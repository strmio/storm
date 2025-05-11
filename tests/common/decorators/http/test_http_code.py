import pytest

from storm.common.constants import HTTP_CODE_METADATA
from storm.common.decorators.http.http_code import HttpCode
from storm.core.di.reflect import Reflect


@pytest.fixture
def sample_handler():
    @HttpCode(201)
    def create_resource():
        return "created"

    return create_resource


def test_http_code_sets_correct_metadata(sample_handler):
    metadata = Reflect.get_metadata(HTTP_CODE_METADATA, sample_handler)
    assert metadata == 201


def test_http_code_metadata_can_be_overwritten():
    @HttpCode(200)
    def handler():
        return "ok"

    Reflect.define_metadata(HTTP_CODE_METADATA, 404, handler)  # override manually
    assert Reflect.get_metadata(HTTP_CODE_METADATA, handler) == 404


def test_http_code_on_multiple_functions():
    @HttpCode(201)
    def post_handler():
        return "created"

    @HttpCode(202)
    def put_handler():
        return "accepted"

    assert Reflect.get_metadata(HTTP_CODE_METADATA, post_handler) == 201
    assert Reflect.get_metadata(HTTP_CODE_METADATA, put_handler) == 202


def test_http_code_decorator_does_not_modify_return_value():
    @HttpCode(200)
    def some_handler():
        return "unchanged"

    assert some_handler() == "unchanged"
