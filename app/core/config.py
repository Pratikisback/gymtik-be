from functools import lru_cache
from typing import Literal

from pydantic import BaseModel, Field, ConfigDict
from pydantic_settings import BaseSettings, SettingsConfigDict


# Base Config Section
class ConfigSection(BaseModel):
    model_config = ConfigDict(
        extra="ignore",
    )

# App Settings
class AppSettings(ConfigSection):
    name: str = "Gymtik"
    version: str = "0.1.0"
    env: Literal["development", "testing", "production"] = "development"
    api_v1_prefix: str = "/api/v1"


# Database Settings
class DatabaseSettings(ConfigSection):
    host: str = "localhost"
    port: int = 5432

    user: str = "gymtik"
    password: str = "gymtik"
    database: str = "gymtik"

    pool_size: int = 10
    max_overflow: int = 20
    pool_timeout: int = 30
        
    @property
    def url(self) -> str:
        return (
            f"postgresql+psycopg://"
            f"{self.user}:{self.password}"
            f"@{self.host}:{self.port}"
            f"/{self.database}"
        )

# Redis Settings
class RedisSettings(ConfigSection):
    url: str = "redis://localhost:6379/0"


# JWT Settings
class JWTSettings(ConfigSection):
    secret_key: str = "HailHitler0987"
    algorithm: str = "HS256"
    access_token_expiry_minutes: int = 5
    refresh_token_expiry_days: int = 7


# Logging Settings
class LoggingSettings(ConfigSection):
    level: Literal[
        "DEBUG",
        "INFO",
        "WARNING",
        "ERROR",
        "CRITICAL",
    ] = "INFO"

    directory: str = "app/logs"
    retention_days: int = 7


# Ollama Settings
class OllamaSettings(ConfigSection):
    base_url: str = "http://localhost:11434"
    llm_model: str = "qwen2.5:7b"
    embedding_model: str = "nomic-embed-text"


# Email Settings (Future)
class EmailSettings(ConfigSection):
    enabled: bool = False
    smtp_host: str = ""
    smtp_port: int = 587
    username: str = ""
    password: str = ""


# Main Settings
class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
        env_nested_delimiter="__"
    )

    app: AppSettings = Field(default_factory=AppSettings)
    database: DatabaseSettings = Field(default_factory=DatabaseSettings)
    redis: RedisSettings = Field(default_factory=RedisSettings)
    jwt: JWTSettings = Field(default_factory=JWTSettings)
    logging: LoggingSettings = Field(default_factory=LoggingSettings)
    ollama: OllamaSettings = Field(default_factory=OllamaSettings)
    email: EmailSettings = Field(default_factory=EmailSettings)

    @property
    def is_development(self) -> bool:
        return self.app.env == "development"

    @property
    def is_testing(self) -> bool:
        return self.app.env == "testing"

    @property
    def is_production(self) -> bool:
        return self.app.env == "production"


@lru_cache
def get_settings() -> Settings:
    return Settings()


settings = get_settings()

