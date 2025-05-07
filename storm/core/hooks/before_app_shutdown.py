from typing import Any, List, Optional

from storm.common.utils import is_function, is_nil


def has_before_application_shutdown_hook(instance: object) -> bool:
    """
    Checks if the given instance has the `before_application_shutdown` function.
    """
    return is_function(getattr(instance, "before_application_shutdown", None))


async def call_operator(instances: List[Any], signal: Optional[str] = None) -> List:
    """
    Calls `before_application_shutdown` on all instances that implement the hook.
    """
    return [
        await instance.before_application_shutdown(signal)
        for instance in instances
        if not is_nil(instance) and has_before_application_shutdown_hook(instance)
    ]


async def call_before_app_shutdown_hook(module, signal: Optional[str] = None) -> None:
    """
    Calls the `before_application_shutdown` function on the module and its children
    (providers, controllers, injectables, middlewares).
    """
    pass
