import unittest

from nightowl.core.config import AppConfig
from nightowl.domain.models import Actor, InboundMessage, UserRole
from nightowl.integrations.sis.mock import MockSISAdapter
from nightowl.services.escalation import EscalationService
from nightowl.services.intent_classifier import IntentClassifier
from nightowl.services.orchestrator import ConversationOrchestrator
from nightowl.services.policy_engine import PolicyEngine


class OrchestratorTests(unittest.TestCase):
    def setUp(self) -> None:
        self.orchestrator = ConversationOrchestrator(
            config=AppConfig(enable_mcp=False),
            sis_adapter=MockSISAdapter(),
            policy_engine=PolicyEngine(),
            intent_classifier=IntentClassifier(),
            escalation_service=EscalationService(),
            mcp_client=None,
        )

    def test_attendance_query_answers(self) -> None:
        msg = InboundMessage(
            tenant_id="sch_1",
            channel="whatsapp",
            text="attendance for today",
            actor=Actor(user_id="p1", role=UserRole.PARENT, linked_student_ids=["s1"]),
        )
        res = self.orchestrator.handle_inbound(msg)
        self.assertEqual("answered", res.status)
        self.assertIn("Attendance status", res.reply_text)

    def test_forbidden_scope_blocked(self) -> None:
        msg = InboundMessage(
            tenant_id="sch_1",
            channel="whatsapp",
            text="show other student attendance",
            actor=Actor(user_id="p1", role=UserRole.PARENT, linked_student_ids=["s1"]),
        )
        res = self.orchestrator.handle_inbound(msg)
        self.assertEqual("blocked", res.status)

    def test_low_confidence_escalates(self) -> None:
        msg = InboundMessage(
            tenant_id="sch_1",
            channel="whatsapp",
            text="hi",
            actor=Actor(user_id="p1", role=UserRole.PARENT, linked_student_ids=["s1"]),
        )
        res = self.orchestrator.handle_inbound(msg)
        self.assertEqual("escalated", res.status)


if __name__ == "__main__":
    unittest.main()
