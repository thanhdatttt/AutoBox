from __future__ import annotations

import os
from dataclasses import dataclass
from urllib.parse import urlparse

from dotenv import load_dotenv


@dataclass(frozen=True)
class Settings:
    ollama_api_key: str
    ollama_base_url: str
    ollama_model: str
    app_timezone: str
    ollama_timeout_seconds: float
    agent_max_tokens: int

    @classmethod
    def from_env(cls) -> "Settings":
        load_dotenv()
        return cls(
            ollama_api_key=os.getenv("OLLAMA_API_KEY", ""),
            ollama_base_url=os.getenv("OLLAMA_BASE_URL", "https://ollama.com/v1"),
            ollama_model=os.getenv("OLLAMA_MODEL", "gpt-oss:20b"),
            app_timezone=os.getenv("APP_TIMEZONE", "Asia/Ho_Chi_Minh"),
            ollama_timeout_seconds=float(os.getenv("OLLAMA_TIMEOUT_SECONDS", "20")),
            agent_max_tokens=int(os.getenv("AGENT_MAX_TOKENS", "512")),
        )

    def require_ollama_credentials(self) -> None:
        missing = []
        if not self.ollama_api_key:
            missing.append("OLLAMA_API_KEY")
        if not self.ollama_base_url:
            missing.append("OLLAMA_BASE_URL")
        if not self.ollama_model:
            missing.append("OLLAMA_MODEL")
        if missing:
            joined = ", ".join(missing)
            raise RuntimeError(f"Missing required Ollama Cloud setting(s): {joined}")

        parsed = urlparse(self.ollama_base_url)
        if parsed.scheme not in {"http", "https"} or not parsed.netloc:
            raise RuntimeError(
                "OLLAMA_BASE_URL must be a full HTTP(S) URL, for example "
                "https://ollama.com/v1"
            )
