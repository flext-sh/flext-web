# Getting Started - flext-web

<!-- TOC START -->
- [Install](#install)
- [Basic Usage](#basic-usage)
- [Working Pattern](#working-pattern)
<!-- TOC END -->

`flext-web` exposes its canonical public facade as `web`.

## Install

```bash
cd flext-web
poetry install
make setup
python -c "from flext_web import web; print('Import successful')"
```

## Basic Usage

```python
from flext_web import web

settings_result = web.settings.create_web_config(
    host="localhost", port=8080, debug=True
)
assert settings_result.success

web.create_fastapi_app()
web.get_service_status()
```

## Working Pattern

- Use `web.settings` for configuration access.
- Use `web.create_fastapi_app()` and `web.create_flask_app()` for framework factories.
- Use `web.start_service()` and `web.stop_service()` for lifecycle control.
- Keep examples and tests on the public facade, not on service classes.
