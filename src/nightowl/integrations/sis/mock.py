from .base import SISAdapter


class MockSISAdapter(SISAdapter):
    """Mock adapter for local development before real SIS wiring."""

    def get_attendance_status(self, tenant_id: str, student_id: str) -> str:
        return "present"
