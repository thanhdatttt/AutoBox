from __future__ import annotations

from dataclasses import dataclass
from datetime import date, timedelta
from zoneinfo import ZoneInfo


@dataclass(frozen=True)
class DateRange:
    start_date: date
    end_date: date

    def as_dict(self) -> dict[str, str]:
        return {
            "start_date": self.start_date.isoformat(),
            "end_date": self.end_date.isoformat(),
        }


class DateResolver:
    def __init__(self, timezone: str) -> None:
        self._timezone = ZoneInfo(timezone)

    def today(self) -> date:
        from datetime import datetime

        return datetime.now(self._timezone).date()

    def resolve(self, expression: str) -> DateRange:
        normalized = expression.strip().lower()
        today = self.today()

        if normalized in {"hôm nay", "hom nay", "today"}:
            return DateRange(today, today)
        if normalized in {"ngày mai", "ngay mai", "tomorrow"}:
            target = today + timedelta(days=1)
            return DateRange(target, target)
        if normalized in {"hôm qua", "hom qua", "yesterday"}:
            target = today - timedelta(days=1)
            return DateRange(target, target)
        if normalized in {"tuần này", "tuan nay", "this week"}:
            return self._week_range(today)
        if normalized in {"tuần sau", "tuan sau", "next week"}:
            return self._week_range(today + timedelta(days=7))
        if normalized in {"tuần trước", "tuan truoc", "last week"}:
            return self._week_range(today - timedelta(days=7))

        parsed = date.fromisoformat(normalized)
        return DateRange(parsed, parsed)

    @staticmethod
    def _week_range(day: date) -> DateRange:
        start = day - timedelta(days=day.weekday())
        return DateRange(start, start + timedelta(days=6))
