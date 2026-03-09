from dataclasses import dataclass

from nightowl.core.config import AppConfig
from nightowl.domain.models import AgentResponse, InboundMessage
from nightowl.domain.world_state import WorldStateBuilder
from nightowl.integrations.mcp.client import MCPClient
from nightowl.integrations.sis.base import SISAdapter
from nightowl.services.escalation import EscalationService
from nightowl.services.intent_classifier import IntentClassifier
from nightowl.services.policy_engine import PolicyEngine


@dataclass(slots=True)
class ConversationOrchestrator:
    config: AppConfig
    sis_adapter: SISAdapter
    policy_engine: PolicyEngine
    intent_classifier: IntentClassifier
    escalation_service: EscalationService
    mcp_client: MCPClient | None = None

    def handle_inbound(self, message: InboundMessage) -> AgentResponse:
        intent = self.intent_classifier.classify(message.text)
        world_state = WorldStateBuilder().build(message, intent)

        # Placeholder confidence from deterministic heuristic.
        confidence = 0.9 if len(message.text.strip()) > 5 else 0.5
        decision = self.policy_engine.evaluate(world_state, confidence)

        if not decision.allowed:
            return AgentResponse(status="blocked", reply_text="Sorry, I can't share that information.", reason=decision.reason)

        if decision.requires_escalation:
            ticket = self.escalation_service.create_ticket(
                tenant_id=message.tenant_id,
                intent=intent,
                reason=decision.reason,
                question=message.text,
            )
            return AgentResponse(
                status="escalated",
                reply_text=f"I have forwarded this to your {ticket.route_to.replace('_', ' ')}.",
                reason=ticket.reason,
            )

        if intent == "attendance_query" and message.actor.linked_student_ids:
            student_id = message.actor.linked_student_ids[0]
            status = self.sis_adapter.get_attendance_status(message.tenant_id, student_id)
            return AgentResponse(status="answered", reply_text=f"Attendance status: {status}.")

        if self.config.enable_mcp and self.mcp_client:
            context = self.mcp_client.fetch_context(message.tenant_id, message.text)
            return AgentResponse(status="answered", reply_text=f"Here's what I found: {context}")

        return AgentResponse(status="answered", reply_text="Thanks. I have recorded your question.")
