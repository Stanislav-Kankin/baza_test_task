from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    # Expected to be provided via env_file / environment variables
    DATABASE_URL: str = "postgresql://app:app@db:5432/app"
    SECRET_KEY: str = "supersecretkey"

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")


settings = Settings()
