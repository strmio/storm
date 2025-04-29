from storm.common.constants import CONTROLLER_WATERMARK, VERSION_METADATA
from storm.core.reflector import Reflector


def Controller(base_path="", middleware=[], version=None):
    """
    A decorator for registering a controller and its routes.

    :param base_path: The base path for the controller's routes.
    :param middleware: Optional middleware to be applied to the controller's routes.
    """

    def decorator(cls):
        Reflector.set_watermark(cls, CONTROLLER_WATERMARK)
        Reflector.set_metadata(cls, "base_path", base_path)
        Reflector.set_metadata(cls, "middleware", middleware)
        Reflector.set_metadata(cls, VERSION_METADATA, version)
        cls.__base_path__ = base_path
        cls.__middleware__ = middleware
        cls.__version__ = version
        return cls

    return decorator
