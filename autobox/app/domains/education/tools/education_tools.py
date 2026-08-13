from __future__ import annotations

from datetime import date

from agents import function_tool

from autobox.app.domains.education.services import EducationService


def build_education_tools(service: EducationService) -> list:
    @function_tool
    def get_students(classroom_id: str | None = None) -> list[dict[str, str]]:
        """Return students, optionally filtered by classroom id."""
        return service.list_students(classroom_id)

    @function_tool
    def search_students(query: str) -> list[dict[str, str]]:
        """Find students by id or name."""
        return service.search_students(query)

    @function_tool
    def get_attendance(start_date: str, end_date: str, status: str | None = None) -> list[dict[str, str]]:
        """Return attendance records between ISO dates, optionally filtered by status."""
        return service.get_attendance(date.fromisoformat(start_date), date.fromisoformat(end_date), status)

    @function_tool
    def record_attendance(student_id: str, attendance_date: str, status: str) -> dict[str, str]:
        """Record present or absent attendance for a student on an ISO date."""
        return service.record_attendance(student_id, date.fromisoformat(attendance_date), status)

    @function_tool
    def get_schedule(start_date: str, end_date: str) -> list[dict[str, str]]:
        """Return class schedule items between ISO dates."""
        return service.get_schedule(date.fromisoformat(start_date), date.fromisoformat(end_date))

    return [get_students, search_students, get_attendance, record_attendance, get_schedule]
