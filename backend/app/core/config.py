from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import Field


class Settings(BaseSettings):
    """Carrega configurações da aplicação via .env e variáveis de ambiente.

    Variáveis suportadas: APP_NAME, APP_VERSION, DEBUG, API_V1_STR, DATABASE_URL, LOG_LEVEL.
    """

    app_name: str = Field(default="Email API", validation_alias="APP_NAME")
    app_version: str = Field(default="0.1.0", validation_alias="APP_VERSION")
    debug: bool = Field(default=False, validation_alias="DEBUG")

    api_v1_str: str = Field(default="/api/v1", validation_alias="API_V1_STR")

    database_url: str = Field(default="", validation_alias="DATABASE_URL")

    log_level: str = Field(default="INFO", validation_alias="LOG_LEVEL")

    model_config = SettingsConfigDict(
        env_file=".env",
        env_prefix="",
        case_sensitive=True,
        extra="ignore",
    )


settings = Settings()