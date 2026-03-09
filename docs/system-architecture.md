# System Architecture

## 1) Product Scope

A multi-tenant SaaS platform where schools can:
- Communicate with parents via WhatsApp (and future channels).
- Use configurable LLM providers (OpenAI, Anthropic, Gemini, local/private models, etc.).
- Let an AI agent answer common school/student questions.
- Escalate low-confidence or restricted questions to class teachers or communication admins.
- Convert teacher rough instructions into formal drafts, route for approval, then publish.

---

## 2) High-Level Architecture

```text
[Parent WhatsApp]
      |
[WhatsApp Business API / BSP]
      |
[Channel Gateway] ---> [Message Normalizer]
      |
[Conversation Orchestrator]
  |        |         |
  |        |         +--> [Policy Engine + World State Guardrails]
  |        +------------> [LLM Router]
  |                       |--> [Provider Adapter: OpenAI]
  |                       |--> [Provider Adapter: Anthropic]
  |                       |--> [Provider Adapter: Azure OpenAI]
  |                       |--> [Provider Adapter: Self-hosted LLM]
  |
  +--> [Knowledge & Data Access Layer]
          |--> [School CMS/ERP connectors]
          |--> [Student Information Service]
          |--> [Attendance/Fees/Events APIs]
          |--> [Vector Search + FAQ Index]

[Escalation Service] <--> [Teacher/Admin Inbox UI]
[Drafting & Approval Service] <--> [Staff Portal]

[Audit Log] [Monitoring/Alerts] [PII Vault/KMS] [RBAC/ABAC IAM]
```

---

## 3) Core Services

### A. Channel Gateway
- Handles WhatsApp webhooks, message receipts, and outbound dispatch.
- Verifies signatures and supports replay-attack protection.
- Normalizes inbound messages (text, voice transcript, image OCR metadata).

### B. Conversation Orchestrator
- Stateful workflow engine for each parent-school thread.
- Invokes policy checks before and after LLM responses.
- Manages intents: query, announcement, escalation, approval loop.

### C. LLM Router (Model-Agnostic)
- Configurable at school level:
  - Default model.
  - Allowed backup models.
  - Cost/latency/quality routing policy.
- Standard interface:
  - `generateResponse(context, policyConstraints)`
  - `classifyIntent(message)`
  - `extractStructuredData(message)`
- Adds provider failover and circuit breakers.

### D. Knowledge & Data Layer
- Unified access facade with per-school isolation.
- Connectors for SIS, attendance, timetable, events, billing, transport.
- Retrieval stack:
  - Policy-filtered retrieval.
  - Metadata filters (class, student, guardian role).
  - Time-scoped context.

### E. Policy Engine + Guardrails
- Enforces world-state boundaries and allowed actions.
- Blocks prohibited outputs (e.g., disclosing another student’s data).
- Confidence/risk scoring:
  - If below threshold => escalate.
  - If sensitive intent detected => force human review.

### F. Escalation Service
- Sends unresolved questions to mapped class teacher or comms admin.
- SLA timers and fallback routing.
- Captures human answer and converts into reusable knowledge snippet.

### G. Drafting & Approval Service
- Teachers submit rough content via UI or WhatsApp staff channel.
- Agent reformats to policy-compliant formal message.
- Approval chain: Teacher -> Admin (optional) -> Publish.
- Full versioning and immutable audit trail.

---

## 4) C4 Container View (Recommended Deployment Units)

1. **edge-api**
   - Public ingress, webhook verification, auth, rate limiting.
2. **conversation-runtime**
   - Turn orchestration, memory/session, policy checkpoints.
3. **policy-service**
   - World-state checks, authorization guardrails, risk classifier.
4. **llm-gateway**
   - Provider adapters, retry/failover, token/cost controls.
5. **school-data-service**
   - Reads/writes to tenant-scoped student/school records.
6. **workflow-service**
   - Escalation tickets, approvals, SLAs, reminders.
7. **notification-service**
   - Outbound WhatsApp templates, status receipts, retries.
8. **audit-service**
   - Append-only compliance logs and evidence exports.

---

## 5) Reference API Contracts

### Parent Query (Inbound)

`POST /v1/messages/inbound`

```json
{
  "tenant_id": "sch_1001",
  "channel": "whatsapp",
  "sender": {"wa_id": "9198XXXXXX", "verified": true},
  "message": {"type": "text", "text": "Is Aarav absent today?"},
  "metadata": {"provider": "meta_cloud", "message_id": "wamid.x"}
}
```

### Escalation Ticket Create

`POST /v1/escalations`

```json
{
  "tenant_id": "sch_1001",
  "thread_id": "thr_443",
  "reason": "low_confidence",
  "route_to": "class_teacher",
  "student_id": "stu_88",
  "question": "Reason for attendance mismatch"
}
```

### Teacher Draft Submission

`POST /v1/drafts`

```json
{
  "tenant_id": "sch_1001",
  "author_user_id": "t_223",
  "source_text": "Tomorrow bring art stuff.",
  "audience": {"class_id": "5A"},
  "channel": "whatsapp"
}
```

---

## 6) Key Runtime Sequences

### A) Parent asks question
1. Inbound webhook verified.
2. Parent identity resolved and mapped to student scope.
3. Policy engine validates requested data scope.
4. Retrieval + LLM generation with constraints.
5. Output DLP and policy post-check.
6. Reply sent OR escalation ticket created.

### B) Teacher rough note to publish
1. Teacher sends rough instruction.
2. Agent creates formal draft (policy/tone template).
3. Approval workflow launched.
4. Approver accepts/edits/rejects.
5. Publish to target audience; store immutable audit trail.

---

## 7) Data Model (Minimum)

- `SchoolTenant`
- `User` (Parent/Teacher/Admin)
- `Student` and `GuardianRelationship`
- `ConversationThread`
- `Message`
- `PolicyRule`
- `EscalationTicket`
- `DraftAnnouncement`
- `ApprovalRecord`
- `KnowledgeDocument`
- `AuditEvent`

All entities include `tenant_id`, timestamps, and provenance metadata.

---

## 8) Integration Architecture

### WhatsApp
- Use Meta WhatsApp Cloud API or BSP (e.g., Twilio, Gupshup, 360dialog).
- Webhook ingest with idempotency keys.
- Template management for proactive notifications.

### School Systems
- Prefer event-driven sync + on-demand read.
- Connector SDK pattern for each ERP/SIS vendor.
- Contract:
  - `getStudentProfile(studentId)`
  - `getAttendance(studentId, dateRange)`
  - `getFeeStatus(studentId)`
  - `getUpcomingEvents(classId)`

---

## 9) Deployment Topology

- Kubernetes-based microservices (or modular monolith in phase 1).
- Per-env isolation: dev/stage/prod.
- Secret management via cloud KMS + vault.
- Message queue for async tasks (escalations, retries, indexing).
- Observability stack: traces, metrics, logs, policy-decision logs.

---

## 10) Reliability Targets

- API availability: 99.9%
- P95 agent response latency: < 3 sec for non-escalated FAQ.
- Escalation dispatch latency: < 30 sec.
- RTO: 2 hours, RPO: 15 minutes.
