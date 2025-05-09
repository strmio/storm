from functools import lru_cache

from pydantic import Field

from storm.core.settings import AppSettings


class Settings(AppSettings):
    app_name: str = "Storm App"

    sys_info_enabled: bool = True
    banner_enabled: bool = True
    banner_file: str = Field(default="banner.txt")


@lru_cache()
def get_settings():
    return Settings()
