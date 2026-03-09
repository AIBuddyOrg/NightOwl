"""Minimal entrypoint showcasing composition of modular services."""

from nightowl.core.config import AppConfig
from nightowl.domain.models import Actor, InboundMessage, UserRole
from nightowl.integrations.mcp.client import MCPClient
from nightowl.integrations.sis.mock import MockSISAdapter
from nightowl.services.escalation import EscalationService
from nightowl.services.intent_classifier import IntentClassifier
from nightowl.services.orchestrator import ConversationOrchestrator
from nightowl.services.policy_engine import PolicyEngine


def build_orchestrator() -> ConversationOrchestrator:
    config = AppConfig(enable_mcp=True, mcp_server_url="http://mcp.local")
    mcp = MCPClient(server_url=config.mcp_server_url) if config.mcp_server_url else None
    return ConversationOrchestrator(
        config=config,
        sis_adapter=MockSISAdapter(),
        policy_engine=PolicyEngine(),
        intent_classifier=IntentClassifier(),
        escalation_service=EscalationService(),
        mcp_client=mcp,
    )


def demo() -> str:
    orchestrator = build_orchestrator()
    response = orchestrator.handle_inbound(
        InboundMessage(
            tenant_id="sch_1001",
            channel="whatsapp",
            text="Is my child absent today?",
            actor=Actor(user_id="p_1", role=UserRole.PARENT, linked_student_ids=["stu_1"]),
        )
    )
    return response.reply_text


if __name__ == "__main__":
    print(demo())
