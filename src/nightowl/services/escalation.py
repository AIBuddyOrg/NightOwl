from dataclasses import dataclass


@dataclass(slots=True)
class EscalationTicket:
    tenant_id: str
    route_to: str
    reason: str
    question: str


class EscalationService:
    def create_ticket(self, tenant_id: str, intent: str, reason: str, question: str) -> EscalationTicket:
        route_to = "class_teacher" if intent != "announcement_request" else "communication_admin"
        return EscalationTicket(
            tenant_id=tenant_id,
            route_to=route_to,
            reason=reason,
            question=question,
        )
