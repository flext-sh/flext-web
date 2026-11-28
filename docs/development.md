# Development Guide - flext-web

<!-- TOC START -->

- [Current Architecture](#current-architecture)
- [Development Workflow](#development-workflow)
- [Public API Rule](#public-api-rule)
- [Settings Rule](#settings-rule)

<!-- TOC END -->

## Current Architecture

`flext-web` is centered on one canonical public facade:

```python
from flext_web import web
```

Current source layout:

- `api.py`: thin public facade and shared `web` instance
- `app.py`: FastAPI app factory
- `base.py`: common service base with typed runtime settings
- `_settings.py`: direct namespaced settings singleton and model
- `services/`: canonical service implementations
- `protocols.py`: runtime protocol and registry behavior
- `models.py`, `constants.py`, `typings.py`, `utilities.py`: SSOT support tiers

## Development Workflow

Run from the active workspace/worktree root. For a standalone checkout, this is
the repository root. In a physical FLEXT workspace, stay at the workspace root;
use `ALL=Y` with test verbs when the run must include every governed member.

```bash
make setup
make check CHECK_PHASE=complete
make tests
```

In a normal local invocation, `make check CHECK_PHASE=complete` regenerates exports and lazy
initialization, applies repairs and formatting, and validates the result. CI and commit hooks
validate committed output without applying those repairs.

## Public API Rule

- Operational code should prefer `web`.
- Tests and examples should exercise the public facade, not internal service classes.
- `api.py` stays thin; behavior belongs in services, settings, protocols or app
  factories.

## Settings Rule

Configuration access is namespaced and direct:

```python
from flext_web import FlextWebSettings, settings
from tests import tm

runtime_settings = FlextWebSettings(
    Web={"host": "localhost", "port": 8080}, debug=settings.debug
)
tm.that(runtime_settings.Web.host, eq="localhost")
```
## Service Rule

Lifecycle operations stay on the facade:

```python
from flext_web import web

assert web.get_service_status().success
assert web.start_service(host="127.0.0.1", port=8080).success
assert web.stop_service().success
```
## Quality Rule

Run complete checks and the native incremental Testmon route:

```bash
make check CHECK_PHASE=complete
make tests
```

Use `make tests-full` when complete test-inventory qualification is required.
In a physical workspace, `make tests ALL=Y` and `make tests-full ALL=Y` include
every governed member.
