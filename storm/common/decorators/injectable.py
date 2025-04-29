from storm.common.constants import INJECTABLE_WATERMARK
from storm.core.reflector import Reflector


def Injectable(singleton=True):
    """
    Mark a class as injectable.
    :param singleton: Boolean indicating if the service should be a singleton.
    """

    def wrapper(cls):
        Reflector.set_watermark(cls, INJECTABLE_WATERMARK)
        Reflector.set_metadata(cls, "__injectable__", True)
        Reflector.set_metadata(cls, "__singleton__", singleton)
        Reflector.set_metadata(cls, "class_name", cls.__name__)
        cls.__injectable__ = True
        cls.__singleton__ = singleton
        return cls

    return wrapper
