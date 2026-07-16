# FLEXT Web Source Guide

`flext_web` exposes one canonical public surface:
`from flext_web import web, c, t, p, m, p, u`.

Everything operational goes through `web`. Structural contracts stay under
`c.Web`, `t.Web`, `u.Web`, `m.Web` and `u.Web`.

## Current Structure

- `api.py`: public facade and shared `web` alias, composed from all service classes
- `base.py`: service base with typed `web` settings access
- `settings.py`: registered settings namespace
- `services/`: canonical service implementations
- `protocols.py`: runtime protocol contracts and registry behavior
- `models.py`, `constants.py`, `typings.py`, `utilities.py`: SSOT support modules

## Public Usage

```python
from flext_web import c, m, p, settings, t, u, web

status = web.service_status()
capabilities = web.api_capabilities()
web_settings = settings.Web
health_service_name = c.Web.SERVICE_NAME
app_request_model = m.Web.AppData
response_payload_type = t.Web.ResponseDict
web_protocol = u.Web.WebService
app_identifier = u.format_app_id("demo")
```

## Runtime Factories

```python
from flext_web import web

fastapi_result = web.create_fastapi_app()
flask_result = web.create_flask_app()
```

## Settings

The package-level `settings.Web` namespace is the runtime SSOT. Use the settings
model only when an external boundary provides explicit overrides.

```python
from flext_web import FlextWebSettings, u

runtime_settings = FlextWebSettings(Web={"host": "localhost", "port": 8080})
assert u.Web.validate_settings(runtime_settings).unwrap()
```

## Services

The service surface is intentionally narrow and should stay behind `web`.
Consumers should not reach into internal modules for lifecycle operations.
