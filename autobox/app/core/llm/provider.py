from __future__ import annotations

from abc import ABC, abstractmethod

from agents import AsyncOpenAI, OpenAIChatCompletionsModel

from autobox.app.core.config import Settings


class LLMProvider(ABC):
    @abstractmethod
    def create_model(self) -> OpenAIChatCompletionsModel:
        """Create an Agents SDK model instance."""


class OllamaLLMProvider(LLMProvider):
    def __init__(self, settings: Settings) -> None:
        settings.require_ollama_credentials()
        self._settings = settings

    def create_model(self) -> OpenAIChatCompletionsModel:
        client = AsyncOpenAI(
            api_key=self._settings.ollama_api_key,
            base_url=self._settings.ollama_base_url.rstrip("/") + "/",
            timeout=self._settings.ollama_timeout_seconds,
        )
        return OpenAIChatCompletionsModel(
            model=self._settings.ollama_model,
            openai_client=client,
        )
