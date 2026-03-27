# Development Guide - flext-web


<!-- TOC START -->
- [Current Architecture](#current-architecture)
- [Development Workflow](#development-workflow)
- [Public API Rule](#public-api-rule)
- [Settings Rule](#settings-rule)
- [Service Rule](#service-rule)
- [Quality Rule](#quality-rule)
<!-- TOC END -->

## Current Architecture

`flext-web` is centered on one canonical public facade:

```python
from flext_web import web
```

Current source layout:

- `api.py`: thin public facade and shared `web` instance
- `app.py`: FastAPI and Flask app factories
- `base.py`: common service base with typed `web.settings`
- `settings.py`: registered namespaced settings model
- `services/`: canonical service implementations
- `protocols.py`: runtime protocol and registry behavior
- `models.py`, `constants.py`, `typings.py`, `utilities.py`: SSOT support tiers

## Development Workflow

Use only repository `make` targets:

```bash
make check PROJECT=flext-web
make test PROJECT=flext-web
make gen PROJECT=flext-web
```

Use `make gen` when exports or lazy initialization need regeneration.

## Public API Rule

- Operational code should prefer `web`.
- Tests and examples should exercise the public facade, not internal service
  classes.
- `api.py` stays thin; behavior belongs in services, settings, protocols or app
  factories.

## Settings Rule

Configuration access is namespaced and direct:

```python
from flext_web import web

config = web.settings
result = web.settings.create_web_config(host="localhost", port=8080)
```

## Service Rule

Lifecycle operations stay on the facade:

```python
from flext_web import web

assert web.get_service_status().is_success
assert web.start_service(host="127.0.0.1", port=8080).is_success
assert web.stop_service().is_success
```

## Quality Rule

Changes are not complete until both commands pass:

```bash
make check PROJECT=flext-web
make test PROJECT=flext-web
```
