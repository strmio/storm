import inspect
from typing import Any

from storm.common.constants import ROUTE_ARGS_METADATA
from storm.common.enums.request_param_type import RouteParamtypes
from storm.common.interfaces.features.pipe_transform import PipeTransform
from storm.core.di.reflect import Reflect


class RouteParamMarker:
    """
    Base class for parameter markers used to describe how values should be extracted from the request.

    Attributes:
        data: The extraction key (e.g., field name).
        pipes: Optional transformation or validation pipes.
        paramtype: The enum value representing the source (e.g., query, body).
    """

    def __init__(self, data: Any = None, *pipes: PipeTransform):
        self.data = data
        self.pipes = pipes
        self.paramtype = None  # To be set by subclass


# Specific parameter marker implementations


class Param(RouteParamMarker):
    """Route parameter extracted from req.params."""

    def __init__(self, data: Any = None, *pipes: PipeTransform):
        super().__init__(data, *pipes)
        self.paramtype = RouteParamtypes.PARAM


class Query(RouteParamMarker):
    """Query parameter extracted from req.query."""

    def __init__(self, data: Any = None, *pipes: PipeTransform):
        super().__init__(data, *pipes)
        self.paramtype = RouteParamtypes.QUERY


class Body(RouteParamMarker):
    """Body content extracted from req.body."""

    def __init__(self, data: Any = None, *pipes: PipeTransform):
        super().__init__(data, *pipes)
        self.paramtype = RouteParamtypes.BODY


class Headers(RouteParamMarker):
    """Header value extracted from req.headers."""

    def __init__(self, data: Any = None, *pipes: PipeTransform):
        super().__init__(data, *pipes)
        self.paramtype = RouteParamtypes.HEADERS


class UploadedFile(RouteParamMarker):
    """Single uploaded file (e.g., from multipart form-data)."""

    def __init__(self, data: Any = None, *pipes: PipeTransform):
        super().__init__(data, *pipes)
        self.paramtype = RouteParamtypes.FILE


class UploadedFiles(RouteParamMarker):
    """Multiple uploaded files."""

    def __init__(self, *pipes: PipeTransform):
        super().__init__(None, *pipes)
        self.paramtype = RouteParamtypes.FILES


class RawBody(RouteParamMarker):
    """Raw request body (Buffer or string)."""

    def __init__(self, *pipes: PipeTransform):
        super().__init__(None, *pipes)
        self.paramtype = RouteParamtypes.RAW_BODY


class Ip(RouteParamMarker):
    """Client IP address."""

    def __init__(self):
        super().__init__(None)
        self.paramtype = RouteParamtypes.IP


class Session(RouteParamMarker):
    """Session object (if middleware is present)."""

    def __init__(self):
        super().__init__(None)
        self.paramtype = RouteParamtypes.SESSION


class Request(RouteParamMarker):
    """Raw request object."""

    def __init__(self):
        super().__init__(None)
        self.paramtype = RouteParamtypes.REQUEST


class Response(RouteParamMarker):
    """Raw response object."""

    def __init__(self):
        super().__init__(None)
        self.paramtype = RouteParamtypes.RESPONSE


class Next(RouteParamMarker):
    """Next function (for middleware)."""

    def __init__(self):
        super().__init__(None)
        self.paramtype = RouteParamtypes.NEXT


class HostParam(RouteParamMarker):
    """Extracts from host or hostname segment."""

    def __init__(self, data: Any = None):
        super().__init__(data)
        self.paramtype = RouteParamtypes.HOST


def register_param_metadata(controller_cls: type, method_name: str) -> None:
    """
    Scans the default parameter values of a method for instances of RouteParamMarker,
    and registers their metadata for runtime extraction.

    Args:
        controller_cls: The class containing the method.
        method_name: The name of the method to inspect.
    """
    method = getattr(controller_cls, method_name)
    sig = inspect.signature(method)
    metadata = {}

    param_index = 0
    for name, param in sig.parameters.items():
        if name == "self":
            continue
        default = param.default
        if isinstance(default, RouteParamMarker):
            key = f"{default.paramtype.value}:{param_index}"
            metadata[key] = {"index": param_index, "data": default.data, "pipes": default.pipes}
        param_index += 1

    Reflect.define_metadata(ROUTE_ARGS_METADATA, metadata, controller_cls, method_name)
