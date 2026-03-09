# NightOwl Windows App (UI Foundation)

This folder contains a modular UI foundation for a Windows desktop control center where school staff can configure:

- School tenant settings
- LLM/model routing
- WhatsApp/SIS/SMS integrations
- MCP server connectivity
- Security and policy guardrails
- Human approval workflows

## Initial deliverables

1. Information architecture and modular component structure.
2. High-fidelity static mockup (`mockups/configuration-dashboard.html`).
3. Tech stack recommendation in `TECH_STACK.md`.

## Planned implementation sequence

1. Bootstrap Tauri + React + TypeScript app.
2. Build shell layout and navigation.
3. Implement feature modules (config, integrations, security, approvals).
4. Add API client layer for backend orchestration services.
