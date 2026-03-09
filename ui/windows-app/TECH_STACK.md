# Windows Desktop UI Tech Stack (NightOwl Control Center)

## 1) Recommended Stack

- **Desktop shell**: Tauri v2 (Windows-first packaging)
- **UI framework**: React 18 + TypeScript
- **Build tool**: Vite
- **State management**: Zustand (modular stores)
- **Server state**: TanStack Query
- **Forms**: React Hook Form + Zod
- **UI kit**: Fluent UI v9 (native Windows look-and-feel)
- **Styling**: CSS variables + design tokens
- **Charts**: Recharts
- **Routing**: React Router
- **Local secure storage**: Tauri plugin-store + OS credential vault for secrets
- **Testing**: Vitest + React Testing Library + Playwright (UI smoke)

## 2) Why this stack

- Fluent UI aligns with Windows UX expectations.
- Tauri keeps app lightweight and secure compared to heavier Electron builds.
- Type-safe forms + schema validation are important for compliance configuration screens.
- Zustand allows feature-level modular state slices (tenants, channels, policies, approvals).

## 3) Module Boundaries

- `components/layout`: shell, navigation, workspace grids.
- `components/config`: tenant and language/model settings.
- `components/integrations`: WhatsApp, SIS, SMS, MCP configuration panels.
- `components/security`: RBAC, policy thresholds, DLP toggles, audit export options.
- `components/approvals`: teacher/admin publishing workflow configuration.

## 4) Integration Surface Reserved for MCP

- Config model includes:
  - `mcp.enabled`
  - `mcp.serverUrl`
  - `mcp.authMode`
  - `mcp.allowedTools`
- UI supports connection testing and tool allow-list policy assignment per tenant.
