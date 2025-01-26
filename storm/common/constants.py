# Metadata keys
MODULE_METADATA = {
    "IMPORTS": "imports",
    "PROVIDERS": "providers",
    "CONTROLLERS": "controllers",
    "EXPORTS": "exports",
}

GLOBAL_MODULE_METADATA = "__module:global__"
HOST_METADATA = "host"
PATH_METADATA = "path"
PARAMTYPES_METADATA = "design:paramtypes"
SELF_DECLARED_DEPS_METADATA = "self:paramtypes"
OPTIONAL_DEPS_METADATA = "optional:paramtypes"
PROPERTY_DEPS_METADATA = "self:properties_metadata"
OPTIONAL_PROPERTY_DEPS_METADATA = "optional:properties_metadata"
SCOPE_OPTIONS_METADATA = "scope:options"
METHOD_METADATA = "method"
ROUTE_ARGS_METADATA = "__routeArguments__"
CUSTOM_ROUTE_ARGS_METADATA = "__customRouteArgs__"
FILTER_CATCH_EXCEPTIONS = "__filterCatchExceptions__"

PIPES_METADATA = "__pipes__"
GUARDS_METADATA = "__guards__"
INTERCEPTORS_METADATA = "__interceptors__"
EXCEPTION_FILTERS_METADATA = "__exceptionFilters__"

# Map enhancer metadata keys to their subtypes
ENHANCER_KEY_TO_SUBTYPE_MAP = {
    GUARDS_METADATA: "guard",
    INTERCEPTORS_METADATA: "interceptor",
    PIPES_METADATA: "pipe",
    EXCEPTION_FILTERS_METADATA: "filter",
}


# Define the type of enhancer subtypes
class EnhancerSubtype:
    GUARD = ENHANCER_KEY_TO_SUBTYPE_MAP[GUARDS_METADATA]
    INTERCEPTOR = ENHANCER_KEY_TO_SUBTYPE_MAP[INTERCEPTORS_METADATA]
    PIPE = ENHANCER_KEY_TO_SUBTYPE_MAP[PIPES_METADATA]
    FILTER = ENHANCER_KEY_TO_SUBTYPE_MAP[EXCEPTION_FILTERS_METADATA]


RENDER_METADATA = "__renderTemplate__"
HTTP_CODE_METADATA = "__httpCode__"
MODULE_PATH = "__module_path__"
HEADERS_METADATA = "__headers__"
REDIRECT_METADATA = "__redirect__"
RESPONSE_PASSTHROUGH_METADATA = "__responsePassthrough__"
SSE_METADATA = "__sse__"
VERSION_METADATA = "__version__"
INJECTABLE_WATERMARK = "__injectable__"
CONTROLLER_WATERMARK = "__controller__"
CATCH_WATERMARK = "__catch__"
ENTRY_PROVIDER_WATERMARK = "__entryProvider__"
