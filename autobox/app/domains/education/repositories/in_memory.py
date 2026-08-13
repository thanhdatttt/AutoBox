from __future__ import annotations

from datetime import date, time

from autobox.app.domains.education.models import AttendanceRecord, ScheduleItem, Student


class InMemoryEducationRepository:
    def __init__(self) -> None:
        self._students = [
            Student(id="SV001", full_name="Nguyen Van A", classroom_id="CLASS-001"),
            Student(id="SV002", full_name="Tran Van B", classroom_id="CLASS-001"),
            Student(id="SV003", full_name="Le Van C", classroom_id="CLASS-001"),
        ]
        self._attendance = [
            AttendanceRecord(student_id="SV001", attendance_date=date(2026, 8, 13), status="present"),
            AttendanceRecord(student_id="SV002", attendance_date=date(2026, 8, 13), status="absent"),
            AttendanceRecord(student_id="SV003", attendance_date=date(2026, 8, 13), status="absent"),
        ]
        self._schedule = [
            ScheduleItem(
                course_code="CSC13112",
                title="Object-Oriented Programming",
                schedule_date=date(2026, 8, 14),
                starts_at=time(8, 0),
                classroom="Room A101",
            )
        ]

    def list_students(self, classroom_id: str | None = None) -> list[Student]:
        if classroom_id is None:
            return list(self._students)
        return [student for student in self._students if student.classroom_id == classroom_id]

    def search_students(self, query: str) -> list[Student]:
        normalized = query.casefold()
        return [
            student
            for student in self._students
            if normalized in student.id.casefold() or normalized in student.full_name.casefold()
        ]

    def get_attendance(self, start_date: date, end_date: date, status: str | None = None) -> list[AttendanceRecord]:
        records = [
            record
            for record in self._attendance
            if start_date <= record.attendance_date <= end_date
        ]
        if status is None:
            return records
        return [record for record in records if record.status == status]

    def upsert_attendance(self, student_id: str, attendance_date: date, status: str) -> AttendanceRecord:
        record = AttendanceRecord(student_id=student_id, attendance_date=attendance_date, status=status)
        self._attendance = [
            existing
            for existing in self._attendance
            if not (existing.student_id == student_id and existing.attendance_date == attendance_date)
        ]
        self._attendance.append(record)
        return record

    def get_schedule(self, start_date: date, end_date: date) -> list[ScheduleItem]:
        return [
            item
            for item in self._schedule
            if start_date <= item.schedule_date <= end_date
        ]
