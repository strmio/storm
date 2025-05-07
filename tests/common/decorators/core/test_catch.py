from storm.common.constants import CATCH_WATERMARK, FILTER_CATCH_EXCEPTIONS
from storm.common.decorators.core.catch import Catch
from storm.core.di.reflect import Reflect


class CustomExceptionA(Exception):
    pass


class CustomExceptionB(Exception):
    pass


def test_catch_decorator_sets_metadata_with_single_exception():
    @Catch(CustomExceptionA)
    class FilterA:
        pass

    assert Reflect.get_metadata(CATCH_WATERMARK, FilterA) is True
    assert Reflect.get_metadata(FILTER_CATCH_EXCEPTIONS, FilterA) == (CustomExceptionA,)


def test_catch_decorator_sets_metadata_with_multiple_exceptions():
    @Catch(CustomExceptionA, CustomExceptionB)
    class FilterAB:
        pass

    assert Reflect.get_metadata(CATCH_WATERMARK, FilterAB) is True
    assert Reflect.get_metadata(FILTER_CATCH_EXCEPTIONS, FilterAB) == (
        CustomExceptionA,
        CustomExceptionB,
    )


def test_catch_decorator_with_no_exceptions():
    @Catch()
    class FilterAll:
        pass

    assert Reflect.get_metadata(CATCH_WATERMARK, FilterAll) is True
    assert Reflect.get_metadata(FILTER_CATCH_EXCEPTIONS, FilterAll) == ()
