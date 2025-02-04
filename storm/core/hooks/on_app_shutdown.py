from typing import List, Optional, Any
from storm.common.utils.shared import is_function, is_nil


def has_on_app_shutdown_hook(instance: object) -> bool:
    """
    Checks if the given instance has the `on_application_shutdown` function.
    """
    return is_function(getattr(instance, "on_application_shutdown", None))


async def call_operator(instances: List[Any], signal: Optional[str] = None) -> List:
    """
    Calls `on_application_shutdown` on all instances that implement the hook.
    """
    return [
        await instance.on_application_shutdown(signal)
        for instance in instances
        if not is_nil(instance) and has_on_app_shutdown_hook(instance)
    ]


async def call_app_shutdown_hook(module, signal: Optional[str] = None) -> None:
    """
    Calls the `on_application_shutdown` function on the module and its children
    (providers, controllers, injectables, middlewares).
    """
    pass
