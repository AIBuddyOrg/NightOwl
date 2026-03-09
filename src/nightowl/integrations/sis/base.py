from abc import ABC, abstractmethod


class SISAdapter(ABC):
    """Adapter contract to keep SIS integrations modular."""

    @abstractmethod
    def get_attendance_status(self, tenant_id: str, student_id: str) -> str:
        raise NotImplementedError
