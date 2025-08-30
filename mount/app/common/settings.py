from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    crm_environment: str = "dev"
    db_url: str
    db_dsn: str
    jwt_secret_key: str
    jwt_expiration_minutes: int = 30
    allowed_origins: list[str] = []

    model_config = SettingsConfigDict(env_file=".env")


settings = Settings()  # type: ignore
