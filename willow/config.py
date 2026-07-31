from pydantic_settings import BaseSettings
from pydantic_settings import SettingsConfigDict


class SignalConfig(BaseSettings):
    device_name: str = "Willow"
    number: str
    owner: str
    log_group: str
    api_key: str
    base_url: str
    prefix: str = "w/"


class Config(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env", env_nested_delimiter="__", extra="ignore"
    )
    signal: SignalConfig
    # database_url: PostgresDsn
    environment: str = "development"
    port: int = 3000
    timezone: str = "Europe/London"


config = Config()  # type: ignore
