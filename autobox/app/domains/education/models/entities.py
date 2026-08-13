from __future__ import annotations

from dataclasses import dataclass
from datetime import date, time


@dataclass(frozen=True)
class Student:
    id: str
    full_name: str
    classroom_id: str


@dataclass(frozen=True)
class AttendanceRecord:
    student_id: str
    attendance_date: date
    status: str


@dataclass(frozen=True)
class ScheduleItem:
    course_code: str
    title: str
    schedule_date: date
    starts_at: time
    classroom: str
