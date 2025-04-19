from pydantic import Field
from typing import List
from functools import lru_cache
from storm.core.settings import DefaultSettings


class Settings(DefaultSettings):
    app_name: str = "Storm App"
    debug: bool = Field(default=True)
    environment: str = Field(default="development")

    # These fields expect DATABASE_URL and SECRET_KEY from .env
    database_url: str = Field(..., alias="DATABASE_URL")
    secret_key: str = Field(..., alias="SECRET_KEY")

    allowed_hosts: List[str] = ["*"]
    log_level: str = "info"
    sys_monitoring_enabled: bool = True
    sys_monitoring_interval: float = 0.1
    monitoring_interval: int = 60
    repl_enabled: bool = True

    class Config:
        env_file = ".env"
        case_sensitive = True
        populate_by_name = True


@lru_cache()
def get_settings():
    return Settings()
