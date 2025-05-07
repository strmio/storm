from storm.common.decorators.core.apply_decorators import ApplyDecorators
from storm.core.di.reflect import Reflect


def test_apply_decorators_combines_multiple_decorators():
    def decorator1(target, key=None, descriptor=None):
        target_fn = descriptor.value if descriptor else target
        Reflect.define_metadata("test:one", True, target_fn)

    def decorator2(target, key=None, descriptor=None):
        target_fn = descriptor.value if descriptor else target
        Reflect.define_metadata("test:two", 42, target_fn)

    class Example:
        @ApplyDecorators(decorator1, decorator2)
        def method(self):
            pass

    fn = Example.__dict__["method"]
    assert Reflect.get_metadata("test:one", fn) is True
    assert Reflect.get_metadata("test:two", fn) == 42
