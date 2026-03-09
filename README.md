# NightOwl

Modular starter implementation for a secure school-parent communication agent.

## Structure

- `src/nightowl/core` - config and shared runtime settings
- `src/nightowl/domain` - domain models and world-state builder
- `src/nightowl/services` - policy, intent, escalation, orchestration
- `src/nightowl/integrations` - adapter interfaces for SIS, SMS, WhatsApp, and MCP extension point
- `src/nightowl/api` - composition entrypoint
- `tests` - unit tests
- `ui/windows-app` - Windows desktop UI foundation, mockups, and stack decisions

## Run tests

```bash
PYTHONPATH=src python -m unittest discover -s tests
```

## Demo

```bash
PYTHONPATH=src python -m nightowl.api.app
```
