# storm/core/settings.py

from pydantic import Field
from pydantic_settings import BaseSettings
from functools import lru_cache
from typing import List


class DefaultSettings(BaseSettings):
    # App Settings
    app_name: str = "Storm App"
    debug: bool = Field(default=True)
    environment: str = Field(default="development")  # or "production"

    # CORS
    allowed_hosts: List[str] = ["*"]

    # Other custom settings
    log_level: str = "info"

    # Syestem monitoring
    sys_monitoring_enabled: bool = Field(default=True)
    sys_monitoring_interval: int = Field(default=3)  # in seconds

    # REPL settings
    repl_enabled: bool = Field(default=False)


@lru_cache()
def get_settings():
    return DefaultSettings()
