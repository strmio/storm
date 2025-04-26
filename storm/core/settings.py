# storm/core/settings.py

from pydantic import Field
from pydantic_settings import BaseSettings
from functools import lru_cache
from typing import List


class AppSettings(BaseSettings):
    # App Settings
    app_name: str = Field(default="Storm App")
    debug: bool = Field(default=True)
    environment: str = Field(default="development")  # or "production"

    # CORS
    allowed_hosts: List[str] = ["*"]

    # Logging settings
    log_level: str = "info"
    log_to_file: bool = Field(default=False)
    log_file_path: str = Field(default="storm.log")
    # log_file_max_size: int = Field(default=10 * 1024 * 1024)  # 10 MB
    # log_file_backup_count: int = Field(default=5)
    # log_file_compression: bool = Field(default=False)
    # log_file_compression_format: str = Field(default="zip")
    # log_file_compression_level: int = Field(default=5)
    # log_to_console: bool = Field(default=True)
    # log_console_format: str = Field(default="%(asctime)s - %(name)s - %(levelname)s - %(message)s")
    # log_console_datefmt: str = Field(default="%Y-%m-%d %H:%M:%S")

    # Syestem monitoring
    sys_monitoring_enabled: bool = Field(default=False)
    sys_monitoring_interval: int = Field(default=3)  # in seconds

    # REPL settings
    repl_enabled: bool = Field(default=False)

    # System information
    sys_info_enabled: bool = Field(default=False)

    # Banner settings
    banner_enabled: bool = Field(default=False)
    banner_file: str = Field(default="banner.txt")

    # Other custom settings


@lru_cache()
def get_settings():
    return AppSettings()
