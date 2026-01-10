from functools import lru_cache

from pydantic import Field, PostgresDsn, computed_field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
    )

    api_title: str = "Life OS API"
    api_version: str = "1.0.0"
    api_description: str = "API para gerenciamento de carreira, finanças e produtividade pessoal."
    debug: bool = Field(default=False, description="Debug mode")

    db_driver: str = Field(default="postgresql", description="Database driver")
    db_user: str = Field(default="postgres", description="Database user")
    db_password: str = Field(default="postgres", description="Database password")
    db_host: str = Field(default="db", description="Database host")
    db_port: int = Field(default=5432, description="Database port")
    db_name: str = Field(default="domestic_budget", description="Database name")

    @computed_field  # type: ignore[misc]
    @property
    def database_url(self) -> PostgresDsn:
        return PostgresDsn.build(
            scheme=f"{self.db_driver}+psycopg",
            username=self.db_user,
            password=self.db_password,
            host=self.db_host,
            port=self.db_port,
            path=self.db_name,
        )

    sqlalchemy_echo: bool = Field(default=False, description="SQLAlchemy echo mode")
    sqlalchemy_pool_size: int = Field(default=10, description="Database pool size")
    sqlalchemy_max_overflow: int = Field(
        default=20, description="Database max overflow"
    )


@lru_cache
def get_settings() -> Settings:
    return Settings()
