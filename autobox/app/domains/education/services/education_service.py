from __future__ import annotations

from datetime import date

from autobox.app.domains.education.repositories import InMemoryEducationRepository


class EducationService:
    def __init__(self, repository: InMemoryEducationRepository) -> None:
        self._repository = repository

    def list_students(self, classroom_id: str | None = None) -> list[dict[str, str]]:
        return [student.__dict__ for student in self._repository.list_students(classroom_id)]

    def search_students(self, query: str) -> list[dict[str, str]]:
        return [student.__dict__ for student in self._repository.search_students(query)]

    def get_attendance(self, start_date: date, end_date: date, status: str | None = None) -> list[dict[str, str]]:
        students_by_id = {student.id: student for student in self._repository.list_students()}
        return [
            {
                "student_id": record.student_id,
                "student_name": students_by_id[record.student_id].full_name,
                "date": record.attendance_date.isoformat(),
                "status": record.status,
            }
            for record in self._repository.get_attendance(start_date, end_date, status)
        ]

    def record_attendance(self, student_id: str, attendance_date: date, status: str) -> dict[str, str]:
        if status not in {"present", "absent"}:
            raise ValueError("status must be either 'present' or 'absent'")
        known_ids = {student["id"] for student in self.list_students()}
        if student_id not in known_ids:
            raise ValueError(f"Unknown student_id: {student_id}")
        record = self._repository.upsert_attendance(student_id, attendance_date, status)
        return {
            "student_id": record.student_id,
            "date": record.attendance_date.isoformat(),
            "status": record.status,
        }

    def get_schedule(self, start_date: date, end_date: date) -> list[dict[str, str]]:
        return [
            {
                "course_code": item.course_code,
                "title": item.title,
                "date": item.schedule_date.isoformat(),
                "starts_at": item.starts_at.strftime("%H:%M"),
                "classroom": item.classroom,
            }
            for item in self._repository.get_schedule(start_date, end_date)
        ]
