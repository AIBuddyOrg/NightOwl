from dataclasses import dataclass, field
from enum import Enum


class UserRole(str, Enum):
    PARENT = "parent"
    TEACHER = "teacher"
    ADMIN = "admin"


@dataclass(slots=True)
class Actor:
    user_id: str
    role: UserRole
    linked_student_ids: list[str] = field(default_factory=list)
    verification_level: str = "phone_verified"


@dataclass(slots=True)
class InboundMessage:
    tenant_id: str
    channel: str
    text: str
    actor: Actor


@dataclass(slots=True)
class AgentResponse:
    status: str
    reply_text: str
    reason: str | None = None
