from __future__ import annotations

import unittest
from datetime import date

from autobox.app.core.date_resolver import DateResolver
from autobox.app.domains.education.repositories import InMemoryEducationRepository
from autobox.app.domains.education.services import EducationService


class DateResolverTest(unittest.TestCase):
    def test_resolves_iso_date(self) -> None:
        resolver = DateResolver("Asia/Ho_Chi_Minh")

        resolved = resolver.resolve("2026-08-13")

        self.assertEqual(resolved.start_date, date(2026, 8, 13))
        self.assertEqual(resolved.end_date, date(2026, 8, 13))


class EducationServiceTest(unittest.TestCase):
    def test_get_absent_attendance(self) -> None:
        service = EducationService(InMemoryEducationRepository())

        records = service.get_attendance(date(2026, 8, 13), date(2026, 8, 13), "absent")

        self.assertEqual([record["student_name"] for record in records], ["Tran Van B", "Le Van C"])

    def test_rejects_unknown_student_write(self) -> None:
        service = EducationService(InMemoryEducationRepository())

        with self.assertRaises(ValueError):
            service.record_attendance("SV999", date(2026, 8, 13), "present")


if __name__ == "__main__":
    unittest.main()
