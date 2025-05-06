# storm/decorators/controller.py

from typing import List, Optional, Type, Union

from storm.common.constants import CONTROLLER_WATERMARK, HOST_METADATA, PATH_METADATA, SCOPE_OPTIONS_METADATA, VERSION_METADATA
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


#
def Controller(prefix_or_options: Union[str, List[str], ControllerOptions, None] = None):
    """
    Decorator to mark a class as a Storm controller.
    """
    default_path = "/"

    if is_undefined(prefix_or_options):
        path = default_path
        host = None
        scope_options = None
        version = None
    elif is_string(prefix_or_options) or isinstance(prefix_or_options, list):
        path = prefix_or_options
        host = None
        scope_options = None
        version = None
    elif isinstance(prefix_or_options, ControllerOptions):
        path = prefix_or_options.path or default_path
        host = prefix_or_options.host
        scope_options = {"scope": prefix_or_options.scope, "durable": prefix_or_options.durable}

        version = prefix_or_options.version
        if isinstance(version, list):
            version = deduplicate_preserve_order(version)
    else:
        raise TypeError("Invalid argument passed to @Controller decorator")

    def decorator(target: Type):
        Reflect.define_metadata(CONTROLLER_WATERMARK, True, target)
        Reflect.define_metadata(PATH_METADATA, path, target)
        Reflect.define_metadata(HOST_METADATA, host, target)
        Reflect.define_metadata(SCOPE_OPTIONS_METADATA, scope_options, target)
        Reflect.define_metadata(VERSION_METADATA, version, target)
        return target

    return decorator
