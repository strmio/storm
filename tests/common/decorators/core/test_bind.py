from storm.common.decorators.core.bind import Bind


def mock_decorator_factory(log, tag):
    def decorator(target, key, index):
        # No convertir `target` en str
        log.append((tag, target, key, index))

    return decorator


def test_bind_applies_parameter_decorators():
    log = []

    class TestController:
        @Bind(mock_decorator_factory(log, "req"), mock_decorator_factory(log, "body"))
        def handler(self, request, body):
            return request, body

    instance = TestController()
    instance.handler("foo", "bar")

    assert len(log) == 2
    assert log[0][0] == "req"
    assert log[1][0] == "body"
    assert log[0][2] == "handler"
    assert log[1][2] == "handler"
    assert log[0][3] == 0
    assert log[1][3] == 1
    assert callable(log[0][1])
    assert log[0][1].__name__ == "handler"
