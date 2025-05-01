from typing import Optional

from storm.core.interfaces.version_options_interface import VersioningOptions


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
        # self.logger = Logger(self.__name__)
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
        self._versioning_options = options

    def get_versioning(self) -> Optional[VersioningOptions]:
        """
        Retrieve the versioning options for the application.

        Returns:
            Optional[VersioningOptions]: The versioning options if configured,
            otherwise None.
        """
        return self._versioning_options
