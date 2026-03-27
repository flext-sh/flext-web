# flext-web Development Reference


<!-- TOC START -->
- [Canonical Entry Point](#canonical-entry-point)
- [Implementation Map](#implementation-map)
- [Development Commands](#development-commands)
- [Runtime Surface](#runtime-surface)
- [Contribution Guardrails](#contribution-guardrails)
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
- `settings.py`: namespaced settings
- `services/`: auth, entities, health and web service layers
- `protocols.py`: runtime registry and protocol-backed operations

## Development Commands

```bash
make check PROJECT=flext-web
make test PROJECT=flext-web
make gen PROJECT=flext-web
```

## Runtime Surface

```python
from flext_web import web

web.settings
web.create_fastapi_app()
web.create_flask_app()
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
