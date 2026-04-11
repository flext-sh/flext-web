# FLEXT Web

`flext-web` exposes its canonical public facade as `web`:

```python
from flext_web import web
```

Use `web.settings` for the registered settings namespace and call operations
through the facade instead of importing service classes directly.

## What it provides

- Application lifecycle and runtime status management
- FastAPI and Flask app factories
- Settings validation through the `web` namespace
- Canonical example and testing surface for the workspace

## Usage

```python
from flext_web import web

settings = web.settings.create_web_config(host="127.0.0.1", port=8080, debug=True).value
app_result = web.create_fastapi_app()
service_result = web.start_service(
    host=settings.host, port=settings.port, debug=settings.debug_mode
)
```

## Status

`flext-web` is intended for development and controlled validation in the
current workspace. Use the facade directly and keep examples aligned with the
public API.
