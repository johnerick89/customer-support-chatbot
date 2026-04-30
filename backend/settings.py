"""Application settings from environment"""

from __future__ import annotations

import os
from functools import lru_cache

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Loads `.env` / process env; used for OpenAI and optional overrides."""

    model_config = SettingsConfigDict(
        env_file=(".env", ".env.local"),
        env_file_encoding="utf-8",
        extra="ignore",
    )

    openai_api_key: str = Field(
        default="",
        description="Required for streaming chat (OpenAI Agents SDK). Env: OPENAI_API_KEY.",
    )

    def apply_openai_env(self) -> None:
        """Ensure the OpenAI client sees the key from pydantic-loaded env files."""
        key = (self.openai_api_key or "").strip()
        if key:
            os.environ.setdefault("OPENAI_API_KEY", key)

    @property
    def openai_configured(self) -> bool:
        return bool((self.openai_api_key or "").strip()) or bool(
            (os.environ.get("OPENAI_API_KEY") or "").strip(),
        )


@lru_cache
def get_settings() -> Settings:
    return Settings()
