# storm/common/decorators/http/render.py

from typing import Callable

from storm.common.constants import RENDER_METADATA
from storm.core.di.reflect import Reflect


class Render:
    """
    Decorator that defines the template to be rendered by a controller route.

    :param template: Name of the template file to render (e.g., "index.html").
    :example: @Render("home.html")
    """

    def __init__(self, template: str):
        self.template = template

    def __call__(self, target: object, key: str | None = None, descriptor: Callable | None = None):
        """
        Assigns render metadata to the route handler.

        :param target: The target object (class or prototype)
        :param key: Method name (if used on a class method)
        :param descriptor: The method itself (used for method decorators)
        """
        if descriptor is not None:
            Reflect.define_metadata(RENDER_METADATA, self.template, descriptor)
            return descriptor

        # If used directly on a function
        Reflect.define_metadata(RENDER_METADATA, self.template, target)
        return target
