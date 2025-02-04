from typing import List, Any
from storm.common.utils import is_function, is_nil


def has_on_app_bootstrap_hook(instance: object) -> bool:
    """
    Checks if the given instance has the `on_application_bootstrap` function.
    """
    return is_function(getattr(instance, "on_application_bootstrap", None))


async def call_operator(instances: List[Any]) -> List:
    """
    Calls `on_application_bootstrap` on all instances that implement the hook.
    """
    return [
        await instance.on_application_bootstrap()
        for instance in instances
        if not is_nil(instance) and has_on_app_bootstrap_hook(instance)
    ]


async def call_module_bootstrap_hook(module) -> None:
    """
    Calls the `on_application_bootstrap` function on the module and its children
    (providers, controllers, injectables, middlewares).
    """
    pass
