# FLEXT Web Source Guide

`flext_web` exposes one canonical public surface:
`from flext_web import web, c, t, p, m, u`.

Everything operational goes through `web`. Structural contracts stay under
`c.Web`, `t.Web`, `p.Web`, `m.Web` and `u.Web`.

## Current Structure

- `api.py`: public facade and shared `web` alias, composed from all service classes
- `base.py`: service base with typed `web` settings access
- `settings.py`: registered settings namespace
- `services/`: canonical service implementations
- `protocols.py`: runtime protocol contracts and registry behavior
- `models.py`, `constants.py`, `typings.py`, `utilities.py`: SSOT support modules

## Public Usage

```python
from flext_web import c, m, p, t, u, web

status = web.get_service_status()
capabilities = web.get_api_capabilities()
config = web.settings
health_service_name = c.Web.WebService.SERVICE_NAME
app_request_model = m.Web.AppData
response_payload_type = t.Web.ResponseDict
web_protocol = p.Web.WebService
app_identifier = u.format_app_id("demo")
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
