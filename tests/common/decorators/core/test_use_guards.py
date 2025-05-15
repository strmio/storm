import pytest

from storm.common.constants import GUARDS_METADATA
from storm.common.decorators.core.use_guards import UseGuards
from storm.common.utils.validate_each import InvalidDecoratorItemException
from storm.core.di.reflect import Reflect


# Dummy guards for testing
class ValidGuard:
    def can_activate(self, context):
        return True


class InvalidGuard:
    pass


class FunctionGuard:
    def __call__(self):
        return self

    def can_activate(self, context):
        return True


def test_use_guards_on_method():
    class TestController:
        @UseGuards(ValidGuard)
        def handler(self):
            pass

    metadata = Reflect.get_metadata(GUARDS_METADATA, TestController.handler)
    assert metadata == [ValidGuard]


def test_use_guards_on_class():
    @UseGuards(ValidGuard)
    class TestController:
        pass

    metadata = Reflect.get_metadata(GUARDS_METADATA, TestController)
    assert metadata == [ValidGuard]


def test_use_guards_with_multiple_guards():
    class AnotherGuard:
        def can_activate(self, context):
            return True

    @UseGuards(ValidGuard, AnotherGuard)
    class TestController:
        pass

    metadata = Reflect.get_metadata(GUARDS_METADATA, TestController)
    assert metadata == [ValidGuard, AnotherGuard]


def test_use_guards_invalid_guard_raises():
    with pytest.raises(InvalidDecoratorItemException) as excinfo:

        @UseGuards(InvalidGuard)
        class InvalidController:
            pass

    assert "Invalid guard passed to @UseGuards() decorator" in str(excinfo.value)
