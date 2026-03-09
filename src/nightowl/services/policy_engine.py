from dataclasses import dataclass

from nightowl.domain.world_state import WorldState


@dataclass(slots=True)
class PolicyDecision:
    allowed: bool
    requires_escalation: bool
    reason: str


class PolicyEngine:
    def evaluate(self, world_state: WorldState, confidence: float) -> PolicyDecision:
        if "read_other_students" in world_state.authority.forbidden_actions and world_state.intent == "other_student_query":
            return PolicyDecision(False, False, "forbidden_scope")

        if confidence < 0.72:
            return PolicyDecision(True, True, "low_confidence")

        return PolicyDecision(True, False, "ok")
