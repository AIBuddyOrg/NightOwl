# Security & Privacy Blueprint

## 1) Security Principles

- Privacy by design and default.
- Least privilege for users, services, and model/tool access.
- Defense in depth (identity, network, app, data, monitoring).
- Secure-by-default tenant isolation.

---

## 2) Data Classification

- **Restricted**: Student PII, health notes, disciplinary records.
- **Confidential**: Parent contact data, fees, attendance.
- **Internal**: School notices, timetable content.
- **Public**: General announcements approved for public channels.

Policies should bind storage, transport, retention, and masking to class.

---

## 3) Identity & Access

- SSO/SAML/OIDC for school staff portal.
- Strong RBAC + ABAC:
  - Parent -> linked students only.
  - Teacher -> assigned classes/sections.
  - Comms admin -> publication rights.
- Step-up verification (OTP) for sensitive parent requests.
- Service-to-service auth via mTLS + short-lived workload identity.

---

## 4) Data Protection Controls

- Encryption in transit: TLS 1.2+
- Encryption at rest: AES-256 with managed keys.
- Envelope encryption for highly sensitive fields.
- Tokenization/pseudonymization in analytics pipelines.
- Secrets stored in vault, never in source code.

---

## 5) LLM-Specific Controls

- Provider risk assessment and DPA review.
- Per-tenant model allow-list.
- Disable training-on-customer-data where possible.
- Prompt redaction service for sensitive fields.
- Output DLP scanner before sending parent-facing response.
- Prompt-injection defenses:
  - strict tool calling policy
  - deny external URL fetch by default
  - immutable system policy envelope per turn

---

## 6) Application Security

- Secure SDLC with mandatory code review.
- SAST, dependency scanning, container scanning.
- API rate limiting and anomaly detection.
- HMAC signature verification on webhooks.
- Idempotency keys to prevent replay issues.

---

## 7) Audit & Compliance

- Immutable audit logs for:
  - data access
  - policy decisions
  - escalations
  - approvals/publications
- Regional data residency controls.
- Retention + deletion workflows (including right-to-erasure where required).
- Compliance mappings (adapt by region): GDPR/FERPA/COPPA equivalents.

---

## 8) Threat Model (Top Risks)

1. **Cross-tenant data leakage**
   - Control: tenant-scoped auth claims + row-level security + contract tests.
2. **Parent impersonation on WhatsApp**
   - Control: periodic step-up OTP for restricted data.
3. **Prompt injection from user text**
   - Control: isolated tool executor + prompt sanitizer + output policy checks.
4. **Malicious/accidental broad announcement**
   - Control: mandatory approval workflow + audience simulation preview.
5. **Credential compromise**
   - Control: hardware-backed key management + secret rotation + just-in-time access.

---

## 9) Incident Response

- Playbooks for suspected data leak, prompt injection, account takeover.
- Severity tiers with notification matrix.
- Forensics-ready logs with chain-of-custody controls.
- Post-incident RCA and control hardening cycle.
