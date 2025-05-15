import pytest

from storm.common.constants import EXCEPTION_FILTERS_METADATA
from storm.common.decorators.core.use_filters import UseFilters
from storm.common.utils.validate_each import InvalidDecoratorItemException
from storm.core.di.reflect import Reflect


class DummyFilter:
    def catch(self, exception, context):
        pass


class InvalidFilter:
    pass


class FilterA:
    def catch(self, e, c):
        pass


class FilterB:
    def catch(self, e, c):
        pass


def test_use_filters_on_method():
    class TestController:
        @UseFilters(DummyFilter)
        def handler(self):
            pass

    metadata = Reflect.get_metadata(EXCEPTION_FILTERS_METADATA, TestController.handler)
    assert metadata == [DummyFilter]


def test_use_filters_on_class():
    @UseFilters(DummyFilter)
    class TestController:
        def handler(self):
            pass

    metadata = Reflect.get_metadata(EXCEPTION_FILTERS_METADATA, TestController)
    assert metadata == [DummyFilter]


def test_use_filters_multiple():
    @UseFilters(FilterA, FilterB)
    class TestController:
        def handler(self):
            pass

    metadata = Reflect.get_metadata(EXCEPTION_FILTERS_METADATA, TestController)
    assert metadata == [FilterA, FilterB]


def test_use_filters_invalid_filter_raises():
    with pytest.raises(InvalidDecoratorItemException):

        @UseFilters(InvalidFilter)
        class InvalidController:
            pass
