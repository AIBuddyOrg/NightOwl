# Implementation Roadmap

## Phase 0: Discovery & Governance (2–4 weeks)
- Stakeholder mapping (school leaders, teachers, IT, legal).
- Data inventory and integration feasibility.
- Define policy baseline and world-state schema.
- Finalize non-functional requirements (SLA, compliance, localization).

**Deliverables**
- Tenant policy baseline v1
- Integration readiness report
- Threat model + compliance checklist

## Phase 1: Foundation MVP (6–8 weeks)
- WhatsApp integration (inbound/outbound).
- Parent identity linking with student records.
- FAQ + events + timetable query flows.
- Basic escalation to teacher/admin inbox.
- Audit logging and baseline security controls.

**Exit Criteria**
- 80%+ FAQ auto-resolution for approved intents.
- 100% escalation path for low-confidence requests.
- PII leakage test suite passes.

## Phase 2: Human-in-the-loop Publishing (4–6 weeks)
- Teacher rough draft intake.
- AI formalization with template/tone policies.
- Approval workflow with version history.
- Controlled publish to WhatsApp broadcast lists.

**Exit Criteria**
- All published messages tied to approved artifact ID.
- Full audit trail available for compliance export.

## Phase 3: Multi-LLM & Advanced Guardrails (4–6 weeks)
- Pluggable LLM provider routing and failover.
- Confidence scoring and policy-based model selection.
- Enhanced DLP and sensitive-intent handling.
- Knowledge feedback loop from resolved escalations.

**Exit Criteria**
- Per-tenant model policy enforced in runtime.
- Cost/latency SLO dashboard operational.

## Phase 4: Scale & Enterprise Readiness (ongoing)
- Tenant self-service onboarding.
- Regional compliance packs.
- Advanced analytics dashboards.
- Chaos/reliability testing and DR drills.

---

## Engineering Workstreams

1. **Platform & Infra**: CI/CD, observability, tenancy isolation.
2. **Core Agent Runtime**: orchestrator, policy engine, LLM router.
3. **Integrations**: WhatsApp + SIS/ERP connectors.
4. **Security & Compliance**: IAM, key management, DLP, auditing.
5. **Ops & Support**: runbooks, on-call, incident workflow.

---

## Acceptance Criteria (Initial Launch)

- Parent can ask student-specific questions and receive policy-compliant answers.
- Unauthorized data access attempts are blocked and logged.
- Low-confidence answers consistently escalate to responsible staff.
- Teacher rough drafts can be formalized, approved, and published with full audit trail.
- Security baseline (encryption, RBAC, logging, webhook verification) is active in production.
