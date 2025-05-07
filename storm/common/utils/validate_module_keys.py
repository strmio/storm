# storm/common/utils/validate_module_keys.py

from storm.common.constants import MODULE_METADATA

INVALID_MODULE_CONFIG_MESSAGE = lambda property: (f"Invalid property '{property}' passed into the @Module() decorator.")

metadata_keys = [
    MODULE_METADATA["IMPORTS"],
    MODULE_METADATA["EXPORTS"],
    MODULE_METADATA["CONTROLLERS"],
    MODULE_METADATA["PROVIDERS"],
]


def validate_module_keys(keys: list[str]) -> None:
    for key in keys:
        if key not in metadata_keys:
            raise ValueError(INVALID_MODULE_CONFIG_MESSAGE(key))
