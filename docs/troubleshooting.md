# Troubleshooting - flext-web

<!-- TOC START -->
- [Import Errors](#import-errors)
- [Settings Issues](#settings-issues)
- [Runtime Issues](#runtime-issues)
- [Quick Checks](#quick-checks)
<!-- TOC END -->

## Import Errors

If importing the public facade fails, verify the workspace and generated exports:

```bash
cd flext-web
python -c "from flext_web import web; print(web.get_service_status())"
make gen
make check PROJECT=flext-web FILES="src/flext_web/api.py src/flext_web/settings.py"
```

## Settings Issues

Use the registered namespace through `web.settings`:

```python
from flext_web import web

config_result = web.settings.create_web_config(host="127.0.0.1", port=8080)
assert config_result.success
```

If validation fails, inspect the field values being passed to the settings factory.

## Runtime Issues

When the service does not start, confirm route initialization and middleware setup:

```python
from flext_web import web

assert web.initialize_routes().success
assert web.configure_middleware().success
assert web.start_service(host="127.0.0.1", port=8080).success
```

## Quick Checks

- Import `web` first.
- Use `web.settings` for configuration.
- Use `web.get_service_status()` for lifecycle state.
- Use `make test PROJECT=flext-web` after code changes.
