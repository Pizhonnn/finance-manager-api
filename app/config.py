from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    # База данных
    POSTGRES_USER: str = "postgres"
    POSTGRES_PASSWORD: str = "admin"
    POSTGRES_DB: str = "postgres"
    POSTGRES_HOST: str = "localhost"
    POSTGRES_PORT: int = 15432

    # Настройки приложения
    APP_NAME: str = "Finance Manager API"
    DEBUG: bool = True

    @property
    def DATABASE_URL(self) -> str:
        return f"postgresql+asyncpg://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}@{self.POSTGRES_HOST}:{self.POSTGRES_PORT}/{self.POSTGRES_DB}"

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")


settings = Settings()
