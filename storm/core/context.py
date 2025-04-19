from contextvars import ContextVar
from .settings import AppSettings


class AppContext:
    """
    AppContext is a utility class that provides a context-local storage for application settings
    using a `ContextVar`. It allows setting and retrieving application settings in a thread-safe
    and context-specific manner.

    Attributes:
        _settings_ctx (ContextVar[AppSettings]): A context variable to store the application
            settings for the current context.

    Methods:
        set_settings(settings: AppSettings):
            Sets the application settings for the current context.

        get_settings() -> AppSettings:
            Retrieves the application settings for the current context. Raises a RuntimeError
            if the settings have not been set.
    """

    _settings_ctx: ContextVar[AppSettings] = ContextVar("app_settings", default=None)

    @classmethod
    def set_settings(cls, settings: AppSettings):
        if cls._settings_ctx.get() is not None:
            raise RuntimeError("Settings have already been set in this context.")
        cls._settings_ctx.set(settings)

    @classmethod
    def get_settings(cls) -> AppSettings:
        settings = cls._settings_ctx.get()
        if settings is None:
            raise RuntimeError("Settings have not been set in AppContext.")
        return settings
