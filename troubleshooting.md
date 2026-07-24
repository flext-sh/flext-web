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
python -c "from flext_web import web; u.Cli.print(web.get_service_status())"
make gen
make check PROJECT=flext-web FILES="src/flext_web/api.py src/flext_web/settings.py"
```

## Settings Issues

Validate explicit overrides through the canonical settings model:

```python
from flext_web import FlextWebSettings, u

runtime_settings = FlextWebSettings(Web={"host": "127.0.0.1", "port": 8080})
assert u.Web.validate_settings(runtime_settings).unwrap()
```

If validation fails, inspect the field values being passed to the settings factory.

## Runtime Issues

When the service does not start, confirm route initialization and middleware setup:

```python notest
from flext_web import web

assert web.initialize_routes().success
assert web.configure_middleware().success
assert web.start_service(host="127.0.0.1", port=8080).success
```

## Quick Checks

- Import `web` and `settings` from the package root.
- Use `settings.Web` for configuration.
- Use `web.get_service_status()` for lifecycle state.
- Use `make test PROJECT=flext-web` after code changes.
