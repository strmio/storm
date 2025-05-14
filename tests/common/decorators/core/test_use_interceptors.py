import pytest

from storm.common.constants import INTERCEPTORS_METADATA
from storm.common.decorators.core.use_inerceptors import UseInterceptors
from storm.common.utils.validate_each import InvalidDecoratorItemException
from storm.core.di.reflect import Reflect


class DummyInterceptor:
    def intercept(self, context, next_):
        return next_()


def test_use_interceptors_on_class():
    @UseInterceptors(DummyInterceptor)
    class TestController:
        pass

    metadata = Reflect.get_metadata(INTERCEPTORS_METADATA, TestController)
    assert metadata == [DummyInterceptor]


def test_use_interceptors_on_method():
    class TestController:
        @UseInterceptors(DummyInterceptor)
        def handler(self):
            pass

    metadata = Reflect.get_metadata(INTERCEPTORS_METADATA, TestController.handler)
    assert metadata == [DummyInterceptor]


def test_use_interceptors_with_multiple():
    class InterceptorOne:
        def intercept(self, context, next_):
            return next_()

    class InterceptorTwo:
        def intercept(self, context, next_):
            return next_()

    @UseInterceptors(InterceptorOne, InterceptorTwo)
    class TestController:
        pass

    metadata = Reflect.get_metadata(INTERCEPTORS_METADATA, TestController)
    assert metadata == [InterceptorOne, InterceptorTwo]


def test_use_interceptors_invalid_raises():
    class InvalidInterceptor:
        pass

    with pytest.raises(InvalidDecoratorItemException) as excinfo:

        @UseInterceptors(InvalidInterceptor)
        class TestController:
            pass

    assert "Invalid interceptor passed to @UseInterceptors() decorator" in str(excinfo.value)
