from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    environment: str = "development"

    database_url: str = ""

    jwt_secret: str = ""
    jwt_refresh_secret: str = ""

    redis_url: str = ""

    ai_api_key: str = ""
    ai_model: str = ""

    cors_origins: str = ""

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )


settings = Settings()