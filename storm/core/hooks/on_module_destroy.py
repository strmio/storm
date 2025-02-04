from typing import List, Any
from storm.common.utils.shared import is_function, is_nil


def has_on_module_destroy_hook(instance: Any) -> bool:
    """
    Checks if the given instance has the `on_module_destroy` function.
    """
    return is_function(getattr(instance, "on_module_destroy", None))


async def call_operator(instances: List[Any]) -> List:
    """
    Calls `on_module_destroy` on all instances that implement the hook.
    """
    return [
        await instance.on_module_destroy()
        for instance in instances
        if not is_nil(instance) and has_on_module_destroy_hook(instance)
    ]


async def call_module_destroy_hook(module) -> None:
    """
    Calls the `on_module_destroy` function on the module and its children
    (providers, controllers, injectables, middlewares).
    """
    pass
