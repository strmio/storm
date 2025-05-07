from functools import lru_cache
from typing import List

from pydantic import Field

from storm.core.settings import AppSettings


class Settings(AppSettings):
    app_name: str = "Storm App"
    debug: bool = Field(default=True)

    # These fields expect DATABASE_URL and SECRET_KEY from .env

    allowed_hosts: List[str] = ["*"]
    log_level: str = "info"

    sys_monitoring_enabled: bool = False

    repl_enabled: bool = False

    sys_info_enabled: bool = True
    banner_enabled: bool = True
    banner_file: str = Field(default="banner.txt")


@lru_cache()
def get_settings():
    return Settings()
