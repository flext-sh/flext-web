# FLEXT Web Source Guide

`flext_web` exposes one canonical public facade, `web`, plus the supporting
namespaces for models, constants, protocols, utilities, handlers and settings.

## Current Structure

- `api.py`: public facade and shared `web` alias
- `app.py`: framework app factories
- `base.py`: service base with typed `web` settings access
- `settings.py`: registered settings namespace
- `services/`: canonical service implementations
- `protocols.py`: runtime protocol contracts and registry behavior
- `models.py`, `constants.py`, `typings.py`, `utilities.py`: SSOT support modules

## Public Usage

```python
from flext_web import web

status = web.get_service_status()
capabilities = web.get_api_capabilities()
config = web.settings
```

## Runtime Factories

```python
from flext_web import web

fastapi_result = web.create_fastapi_app()
flask_result = web.create_flask_app()
```

## Settings

`web.settings` is the registered namespace. Use it directly instead of creating
parallel config accessors.

```python
from flext_web import web

config_result = web.settings.create_web_config(host="localhost", port=8080)
```

## Services

The service surface is intentionally narrow and should stay behind `web`.
Consumers should not reach into internal modules for lifecycle operations.
