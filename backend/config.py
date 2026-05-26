from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import field_validator


class Settings(BaseSettings):

    # LLM 

    # MODELS

    # APP

    # FILES

    # VALIDATION
    @field_validator("*")
    @classmethod
    def not_empty(cls, value):
        if isinstance(value, str) and not value.strip():
            raise ValueError("Environment variable cannot be empty")
        return value

    model_config = SettingsConfigDict(
        env_file=".env",
        extra="ignore"
    )


settings = Settings()