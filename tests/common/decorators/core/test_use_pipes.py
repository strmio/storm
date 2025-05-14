from typing import Any

import pytest

from storm.common.constants import PIPES_METADATA
from storm.common.decorators.core.use_pipes import UsePipes
from storm.common.utils.validate_each import InvalidDecoratorItemException
from storm.core.di.reflect import Reflect


class DummyPipe:
    def transform(self, value: Any, metadata: Any) -> Any:
        return value


def test_use_pipes_on_method():
    class TestController:
        @UsePipes(DummyPipe)
        def handler(self):
            pass

    metadata = Reflect.get_metadata(PIPES_METADATA, TestController.handler)
    assert metadata == [DummyPipe]


def test_use_pipes_on_class():
    @UsePipes(DummyPipe)
    class TestController:
        def handler(self):
            pass

    metadata = Reflect.get_metadata(PIPES_METADATA, TestController)
    assert metadata == [DummyPipe]


def test_use_pipes_with_multiple_pipes():
    class PipeOne:
        def transform(self, value, metadata):
            return value

    class PipeTwo:
        def transform(self, value, metadata):
            return value

    @UsePipes(PipeOne, PipeTwo)
    class TestController:
        pass

    metadata = Reflect.get_metadata(PIPES_METADATA, TestController)
    assert metadata == [PipeOne, PipeTwo]


def test_use_pipes_invalid_item_raises():
    class InvalidPipe:
        pass  # no transform method

    with pytest.raises(InvalidDecoratorItemException) as excinfo:

        @UsePipes(InvalidPipe)
        class InvalidController:
            pass

    assert "Invalid pipe passed to @UsePipes() decorator" in str(excinfo.value)
