from __future__ import annotations

import argparse
import sys

from openai import OpenAI

from autobox.app.core.agent import build_autobox_agent
from autobox.app.core.config import Settings
from autobox.app.core.date_resolver import DateResolver
from autobox.app.core.llm import OllamaLLMProvider
from autobox.app.core.tools import build_date_tools
from autobox.app.domains.education.repositories import InMemoryEducationRepository
from autobox.app.domains.education.services import EducationService
from autobox.app.domains.education.tools import build_education_tools


def create_agent() -> object:
    settings = Settings.from_env()
    date_resolver = DateResolver(settings.app_timezone)
    education_service = EducationService(InMemoryEducationRepository())
    tools = [
        *build_date_tools(date_resolver),
        *build_education_tools(education_service),
    ]
    model = OllamaLLMProvider(settings).create_model()
    return build_autobox_agent(model=model, tools=tools, max_tokens=settings.agent_max_tokens)


def check_ollama() -> str:
    settings = Settings.from_env()
    settings.require_ollama_credentials()
    client = OpenAI(
        api_key=settings.ollama_api_key,
        base_url=settings.ollama_base_url.rstrip("/") + "/",
        timeout=settings.ollama_timeout_seconds,
    )
    response = client.chat.completions.create(
        model=settings.ollama_model,
        messages=[{"role": "user", "content": "Reply with only OK."}],
        max_tokens=8,
    )
    return response.choices[0].message.content or "OK"


def main() -> None:
    parser = argparse.ArgumentParser(description="Run the Autobox agent with Ollama Cloud.")
    parser.add_argument("prompt", nargs="?", help="Natural-language task for the agent.")
    parser.add_argument("--check-ollama", action="store_true", help="Run a short Ollama model connectivity check.")
    args = parser.parse_args()

    if args.check_ollama:
        try:
            print(check_ollama())
        except Exception as error:
            print(f"Ollama check failed: {error}", file=sys.stderr)
            raise SystemExit(2) from error
        return

    prompt = args.prompt or input("Autobox> ")
    try:
        agent = create_agent()
        print(agent.run(prompt))
    except RuntimeError as error:
        print(f"Configuration error: {error}", file=sys.stderr)
        raise SystemExit(2) from error


if __name__ == "__main__":
    main()
