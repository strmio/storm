from typing import Union, List, Pattern, Callable, Optional, Protocol, Any

# Static Origin types: boolean | string | RegExp | (string | RegExp)[]
StaticOrigin = Union[bool, str, Pattern[str], List[Union[str, Pattern[str]]]]


# Callback for the custom origin function
class CustomOriginCallback(Protocol):
    def __call__(
        self, err: Optional[Exception], origin: Optional[StaticOrigin] = None
    ) -> None: ...


# Equivalent of CustomOrigin type
CustomOrigin = Callable[[str, CustomOriginCallback], None]


# CORS Options interface
class CorsOptions:
    def __init__(
        self,
        origin: Optional[Union[StaticOrigin, CustomOrigin]] = None,
        methods: Optional[Union[str, List[str]]] = None,
        allowed_headers: Optional[Union[str, List[str]]] = None,
        exposed_headers: Optional[Union[str, List[str]]] = None,
        credentials: Optional[bool] = None,
        max_age: Optional[int] = None,
        preflight_continue: Optional[bool] = None,
        options_success_status: Optional[int] = None,
    ):
        self.origin = origin
        self.methods = methods
        self.allowed_headers = allowed_headers
        self.exposed_headers = exposed_headers
        self.credentials = credentials
        self.max_age = max_age
        self.preflight_continue = preflight_continue
        self.options_success_status = options_success_status


# Callback for CorsOptionsDelegate
class CorsOptionsCallback(Protocol):
    def __call__(self, error: Optional[Exception], options: CorsOptions) -> None: ...


# CORS Options Delegate
CorsOptionsDelegate = Callable[[Any, CorsOptionsCallback], None]
