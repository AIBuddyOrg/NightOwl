# World State & Agent Boundaries

This document defines the **World State** to constrain agent behavior and prevent unsafe or unauthorized actions.

## 1) World State Schema

```json
{
  "tenant_id": "sch_1001",
  "actor": {
    "role": "parent",
    "user_id": "p_882",
    "verification_level": "otp_verified",
    "linked_student_ids": ["stu_88", "stu_89"]
  },
  "conversation": {
    "thread_id": "thr_443",
    "intent": "attendance_query",
    "language": "en",
    "channel": "whatsapp"
  },
  "authority": {
    "allowed_actions": ["read_attendance", "read_timetable"],
    "forbidden_actions": ["publish_announcement", "read_other_students"]
  },
  "knowledge": {
    "sources": ["sis", "events_db", "policy_docs"],
    "max_data_staleness_mins": 60
  },
  "risk": {
    "confidence_threshold": 0.72,
    "sensitive_intent": false,
    "requires_human_review": false
  }
}
```

---

## 2) World State Layers

1. **Identity State**
   - Who is messaging? (parent identity, linked students, role)
   - Verification level (phone verified, OTP verified, unknown)

2. **Context State**
   - Active school term/calendar.
   - Student/class associations.
   - Current conversation intent and topic.

3. **Authority State**
   - What data/actions user can access.
   - Parent can view only own child records.
   - Teacher/admin can act only within assigned scope.

4. **Knowledge State**
   - Approved source-of-truth datasets.
   - Last synchronization timestamp.
   - Confidence score per answer source.

5. **Operational State**
   - Model health, fallback availability.
   - Escalation queue and SLA status.

---

## 3) Hard Boundaries (Non-Negotiable)

- Never reveal one student’s data to another parent.
- Never fabricate policy/fees/attendance if authoritative data unavailable.
- Never issue disciplinary or medical advice beyond predefined templates.
- Never publish school-wide communication without required approvals.
- Never execute admin action from parent channel.

---

## 4) Decision Matrix

### Auto-Answer Allowed
- High confidence + non-sensitive + authorized data access.
- Example: “What are tomorrow’s class timings?”

### Clarification Required
- Missing student context or ambiguous intent.
- Example: parent linked to multiple children asks “attendance today?”

### Human Escalation Required
- Low confidence.
- Sensitive or exceptional cases.
- Policy/disciplinary disputes.
- Potential legal/privacy issue.

### Approval Required Before Publish
- Any outbound broadcast or class/group announcement.
- Any message generated from teacher rough notes.

---

## 5) Policy Checkpoints (Per Turn)

1. **Pre-retrieval authorization check**
   - Is actor allowed to query this student/entity?
2. **Tool permission check**
   - Which backend tools may be called this turn?
3. **Pre-send output check**
   - DLP + boundary policy scan on model output.
4. **Escalation decision check**
   - Confidence/risk threshold cross?
5. **Audit completeness check**
   - Persist request, decision path, final action.

---

## 6) Escalation Routing Rules

1. Route to class teacher if question is class/student specific.
2. Route to communication admin if institutional policy/public communication.
3. Escalate to principal/authorized authority for severity flags:
   - Bullying/safety concerns.
   - Legal threats.
   - Data breach suspicion.

SLA example:
- Teacher response expected in 2h during school hours.
- Auto-reminder after 30 min and 90 min.
- Auto-reassign after SLA breach.

---

## 7) Human-in-the-Loop Draft Workflow

1. Teacher submits rough instruction.
2. Agent converts to formal draft with tone and policy checks.
3. System validates PII and prohibited content.
4. Approver reviews diff vs rough input.
5. On approval, publish through selected channels.
6. Persist final artifact + approval metadata for audit.

---

## 8) Prompt/Policy Envelope (Concept)

Every model call should include:
- Tenant policy rules.
- User role and permitted student IDs.
- Allowed tools for this turn.
- Prohibited topics/actions.
- Required action on uncertainty: ask clarifying question or escalate.
