from dataclasses import dataclass

from .models import Actor, InboundMessage


@dataclass(slots=True)
class AuthorityState:
    allowed_actions: list[str]
    forbidden_actions: list[str]


@dataclass(slots=True)
class WorldState:
    tenant_id: str
    actor: Actor
    intent: str
    authority: AuthorityState


class WorldStateBuilder:
    """Builds constrained world-state for each turn."""

    def build(self, message: InboundMessage, intent: str) -> WorldState:
        if message.actor.role.value == "parent":
            allowed = ["read_attendance", "read_timetable", "read_events"]
            forbidden = ["publish_announcement", "read_other_students"]
        else:
            allowed = ["read_attendance", "read_timetable", "publish_announcement"]
            forbidden = []

        return WorldState(
            tenant_id=message.tenant_id,
            actor=message.actor,
            intent=intent,
            authority=AuthorityState(allowed_actions=allowed, forbidden_actions=forbidden),
        )
