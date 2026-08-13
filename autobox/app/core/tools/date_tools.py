from __future__ import annotations

from agents import function_tool

from autobox.app.core.date_resolver import DateResolver


def build_date_tools(date_resolver: DateResolver) -> list:
    @function_tool
    def resolve_date(expression: str) -> dict[str, str]:
        """Resolve Vietnamese or English relative dates into ISO date boundaries."""
        return date_resolver.resolve(expression).as_dict()

    return [resolve_date]
