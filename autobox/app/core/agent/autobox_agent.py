from __future__ import annotations

from agents import Agent, ModelSettings, RunConfig, Runner


AGENT_INSTRUCTIONS = """
You are Autobox, a workflow automation agent for business processes.

Core rules:
- Use tools for business data. Do not invent students, attendance, schedules, or records.
- Resolve relative dates with the date tool before calling business tools.
- Ask a clarification question when a write action is missing a required critical parameter.
- Keep final responses concise and natural. Vietnamese is preferred when the user writes Vietnamese.
- Write operations must use validated tools only.
""".strip()


class AutoboxAgent:
    def __init__(self, agent: Agent) -> None:
        self._agent = agent

    def run(self, user_request: str) -> str:
        result = Runner.run_sync(
            self._agent,
            user_request,
            run_config=RunConfig(tracing_disabled=True),
        )
        return str(result.final_output)


def build_autobox_agent(model: object, tools: list, max_tokens: int = 512) -> AutoboxAgent:
    agent = Agent(
        name="Autobox",
        instructions=AGENT_INSTRUCTIONS,
        model=model,
        model_settings=ModelSettings(max_tokens=max_tokens),
        tools=tools,
    )
    return AutoboxAgent(agent)
