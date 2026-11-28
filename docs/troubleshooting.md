# Troubleshooting - flext-web

<!-- TOC START -->

- [Import Errors](#import-errors)
- [Settings Issues](#settings-issues)

<!-- TOC END -->

## Import Errors

If importing the public facade fails, verify the workspace and generated exports.
Run from the active workspace/worktree root. For a standalone checkout, this is
the repository root. In a physical FLEXT workspace, stay at the workspace root;
use `ALL=Y` with test verbs when the run must include every governed member.

```bash
make setup
make check CHECK_PHASE=complete
python -c "from flext_web import u, web; u.Cli.print(web.get_service_status())"
```

## Settings Issues

Validate explicit overrides through the canonical settings model:

```python
from flext_web import FlextWebSettings

runtime_settings = FlextWebSettings(Web={"host": "127.0.0.1", "port": 8080})
assert runtime_settings.Web.host == "127.0.0.1"
assert runtime_settings.Web.port == 8080
```
The constructor validates the declared fields. If it raises a validation error,
inspect the values passed to the settings model.

## Runtime Issues

When the service does not start, confirm route initialization and middleware setup:

```python
from flext_web import web

assert web.initialize_routes().success
assert web.configure_middleware().success
assert web.start_service(host="127.0.0.1", port=8080).success
```
## Quick Checks

- Import `web` and `settings` from the package root.
- Use `settings.Web` for configuration.
- Use `web.get_service_status()` for lifecycle state.
- Run `make check CHECK_PHASE=complete` and `make tests` after code changes.
