# storm/decorators/controller.py

from typing import List, Optional, Type, Union

from storm.common.constants import (
    CONTROLLER_WATERMARK,
    HOST_METADATA,
    PATH_METADATA,
    SCOPE_OPTIONS_METADATA,
    VERSION_METADATA,
)
from storm.common.interfaces.scope_options import Scope, ScopeOptions
from storm.common.interfaces.version_options import VersionOptions, VersionValue
from storm.common.utils.shared import deduplicate_preserve_order, is_string, is_undefined
from storm.core.di.reflect import Reflect


class ControllerOptions(ScopeOptions, VersionOptions):
    def __init__(
        self,
        path: Optional[Union[str, List[str]]] = None,
        host: Optional[Union[str, List[str]]] = None,
        version: Optional[VersionValue] = None,
        scope: Optional[Scope] = None,
        durable: Optional[bool] = None,
    ):
        ScopeOptions.__init__(self, scope, durable)
        VersionOptions.__init__(self, version)
        self.path = path or "/"
        self.host = host


class Controller:
    """
    Class decorator that marks a class as a Storm controller.
    """

    def __init__(self, prefix_or_options: Union[str, List[str], ControllerOptions, None] = None):
        self.default_path = "/"
        self.path: Union[str, List[str]] = self.default_path
        self.host: Optional[Union[str, List[str]]] = None
        self.scope_options: Optional[dict] = None
        self.version: Optional[VersionValue] = None

        if is_undefined(prefix_or_options):
            pass
        elif is_string(prefix_or_options) or isinstance(prefix_or_options, list):
            self.path = prefix_or_options
        elif isinstance(prefix_or_options, ControllerOptions):
            self.path = prefix_or_options.path or self.default_path
            self.host = prefix_or_options.host
            self.scope_options = {
                "scope": prefix_or_options.scope,
                "durable": prefix_or_options.durable,
            }

            version = prefix_or_options.version
            if isinstance(version, list):
                version = deduplicate_preserve_order(version)
            self.version = version
        else:
            raise TypeError("Invalid argument passed to @Controller decorator")

    def __call__(self, target: Type) -> Type:
        Reflect.define_metadata(CONTROLLER_WATERMARK, True, target)
        Reflect.define_metadata(PATH_METADATA, self.path, target)
        Reflect.define_metadata(HOST_METADATA, self.host, target)
        Reflect.define_metadata(SCOPE_OPTIONS_METADATA, self.scope_options, target)
        Reflect.define_metadata(VERSION_METADATA, self.version, target)
        return target
