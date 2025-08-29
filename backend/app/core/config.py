from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import Field


class Settings(BaseSettings):
    """Carrega configurações da aplicação via .env e variáveis de ambiente."""

    app_name: str = Field(validation_alias="APP_NAME")
    app_version: str = Field(validation_alias="APP_VERSION")
    debug: bool = Field(validation_alias="DEBUG")

    api_v1_str: str = Field(validation_alias="API_V1_STR")

    database_url: str = Field(validation_alias="DATABASE_URL")

    log_level: str = Field(validation_alias="LOG_LEVEL")

    model_config = SettingsConfigDict(
        env_file=".env",
        env_prefix="",
        case_sensitive=True,
        extra="ignore",
    )


settings = Settings()