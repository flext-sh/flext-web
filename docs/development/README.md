# flext-web Development Reference

<!-- TOC START -->

- [Canonical Entry Point](#canonical-entry-point)
- [Implementation Map](#implementation-map)
- [Development Commands](#development-commands)
- [Runtime Surface](#runtime-surface)

<!-- TOC END -->

This reference tracks the current implementation, not historical or target
architectures.

## Canonical Entry Point

```python
from flext_web import web
```

## Implementation Map

- `api.py`: public facade
- `app.py`: framework app factories
- `base.py`: service base
- `_settings.py`: namespaced settings
- `services/`: auth, entities, health and web service layers
- `protocols.py`: runtime registry and protocol-backed operations

## Development Commands

Run from the active workspace/worktree root. For a standalone checkout, this is
the repository root. In a physical FLEXT workspace, stay at the workspace root;
use `ALL=Y` with test verbs when the run must include every governed member.

```bash
make setup
make check CHECK_PHASE=complete
make tests
```

`make tests` uses the persistent Testmon selection. Use `make tests-full` for the
complete selected inventory, adding `ALL=Y` in a workspace to include its members.

## Runtime Surface

```python
from flext_web import web

web.settings
web.create_fastapi_app()
web.create_app(...)
web.start_app(...)
web.start_service(...)
web.stop_service()
```
## Contribution Guardrails

- Keep `api.py` thin.
- Keep services in `src/flext_web/services/`.
- Use `web` as the public operational surface in tests and examples.
- Do not document or reintroduce obsolete helpers such as
  `create_web_service`, `get_web_settings`, `reset_web_settings`,
  `validate_config` or direct `service.run()` flows.
