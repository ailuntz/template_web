import re

from pydantic import field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
    )

    # Application
    app_name: str = "MyApp"
    debug: bool = False
    secret_key: str = "change-me-in-production"

    # Database
    database_url: str = "postgresql+psycopg://user:password@localhost:5432/myapp"

    # JWT
    jwt_secret_key: str = "change-me-in-production"
    jwt_algorithm: str = "HS256"
    jwt_access_token_expire_minutes: int = 60
    jwt_refresh_token_expire_days: int = 30

    # Registration
    registration_institution_code: str | None = None

    # Sentry
    sentry_dsn: str | None = None

    # CORS
    cors_origins: list[str] = ["http://localhost:5173", "http://localhost:3000"]

    @field_validator("registration_institution_code")
    @classmethod
    def validate_registration_institution_code(cls, value: str | None) -> str | None:
        if value in (None, ""):
            return None
        if not re.fullmatch(r"\d{6}", value):
            raise ValueError("REGISTRATION_INSTITUTION_CODE must be exactly 6 digits")
        return value


settings = Settings()
