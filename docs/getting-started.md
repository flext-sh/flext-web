# Getting Started - flext-web

<!-- TOC START -->

- [Install](#install)
- [Basic Usage](#basic-usage)
- [Working Pattern](#working-pattern)

<!-- TOC END -->

`flext-web` exposes its canonical public facade as `web`.

## Install

```bash
make setup
```

## Basic Usage

```python
from flext_web import web

app_result = web.create_fastapi_app()
app = app_result.unwrap()
```

To serve the application over HTTP, run the public launcher:

```bash
flext-web run
```

The launcher uses `settings.Web.host` and `settings.Web.port`, blocks while
Uvicorn serves the application, and exposes `/health` and `/info`. Use `--host`
and `--port` for explicit bind overrides. The facade lifecycle methods manage
application state; they do not themselves open a network listener.

## Working Pattern

- Import `settings` from `flext_web` and use `settings.Web` for runtime settings.
- Use `web.create_fastapi_app()` and `web.create_flask_app()` for framework factories.
- Use `web.start_service()` and `web.stop_service()` for lifecycle control.
- Keep examples and tests on the public facade, not on service classes.
