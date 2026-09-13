from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    ENV: str = "development"
    EVENT_STORE_TYPE: str = "in_memory"
    BASIC_RPS: int = 5000
    PRO_RPS: int = 12000


settings = Settings()
