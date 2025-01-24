from pathlib import Path

import yaml
from pydantic import BaseModel, SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict


class ServiceSettings(BaseModel):
    """Service settings."""

    title: str
    description: str
    host: str
    port: int
    debug: bool
    base_url: str


class DatabaseSettings(BaseModel):
    """Database settings."""

    host: str
    port: int
    name: str
    username: str
    echo: bool


class Secrets(BaseSettings):
    """Secrets settings."""

    db_password: SecretStr = SecretStr('password')

    model_config = SettingsConfigDict(
        env_file=".env", env_file_encoding="utf-8"
    )


class AppConfig(BaseSettings):
    """Main configuration class."""

    service: ServiceSettings
    db: DatabaseSettings
    secrets: Secrets

    model_config = SettingsConfigDict(
        env_file='.env',
        env_file_encoding='utf-8',
        case_sensitive=False,
    )

    @classmethod
    def load_settings(cls, file_path: str) -> 'AppConfig':
        """Load configuration from YAML and environment variables."""
        yaml_config = yaml.safe_load(
            Path(file_path).read_text(encoding='utf-8')
        )
        return cls(**yaml_config, secrets=Secrets())

    def _build_db_url(self, driver: str) -> str:
        """Create database URL method."""
        return (
            f'postgresql+{driver}://{self.db.username}:'
            f'{self.secrets.db_password.get_secret_value()}@'
            f'{self.db.host}:{self.db.port}/{self.db.name}'
        )

    @property
    def async_db_url(self) -> str:
        """Async database URL."""
        return self._build_db_url("asyncpg")

    @property
    def sync_db_url(self) -> str:
        """Sync database URL."""
        return self._build_db_url("psycopg2")


config = AppConfig.load_settings("src/config/config.yaml")
