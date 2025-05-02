import inspect
from typing import Dict, Any, Type, Optional
from storm.common.enums.versioning_type import VersioningType
from storm.core.interfaces.version_options_interface import (
    CustomVersioningOptions,
    HeaderVersioningOptions,
    MediaTypeVersioningOptions,
    UriVersioningOptions,
    VersioningOptions,
)


VERSIONING_CLASS_MAP: Dict[VersioningType, Type[VersioningOptions]] = {
    VersioningType.HEADER: HeaderVersioningOptions,
    VersioningType.URI: UriVersioningOptions,
    VersioningType.MEDIA_TYPE: MediaTypeVersioningOptions,
    VersioningType.CUSTOM: CustomVersioningOptions,
}


class ApplicationConfig:
    """
    A class to manage application configuration, specifically for versioning options.

    Methods:
        enable_versioning(options: VersioningOptions):
            Enables versioning for the application by setting the versioning options.
            If the `default_version` attribute of the options is a list, duplicates
            are removed while preserving the order.

        get_versioning() -> Optional[VersioningOptions]:
            Retrieves the current versioning options if they are set, otherwise returns None.
    """

    def __init__(self):
        self._versioning_options: Optional[VersioningOptions] = None

    def enable_versioning(self, options: VersioningOptions):
        """
         Enables versioning for the application by configuring the provided versioning options.

        : options (VersioningOptions): An object containing versioning configuration.
             If the `default_version` attribute exists and is a list, duplicates
             will be removed while preserving the order.

         Side Effects:
             - Updates the `_versioning_options` attribute with the provided options.

         Note:
             The `default_version` attribute of `options` will be modified in-place
             if it is a list.
        """
        if hasattr(options, "default_version") and isinstance(
            options.default_version, list
        ):
            options.default_version = list(dict.fromkeys(options.default_version))
        self._versioning_options = self._init_versioning(options)

    def get_versioning(self) -> Optional[VersioningOptions]:
        """
        Retrieve the versioning options for the application.

        Returns:
            Optional[VersioningOptions]: The versioning options if configured,
            otherwise None.
        """
        if self._versioning_options:
            return self._versioning_options

    @staticmethod
    def _init_versioning(versioning_options: Dict[str, Any]) -> VersioningOptions:
        versioning_type = versioning_options.get("type")
        cls = VERSIONING_CLASS_MAP.get(versioning_type)

        if cls is None:
            raise ValueError(f"Unsupported versioning type: {versioning_type}")

        # Get init signature (excluding 'self')
        sig = inspect.signature(cls.__init__)
        params = {k: v for k, v in versioning_options.items() if k in sig.parameters}

        return cls(**params)
