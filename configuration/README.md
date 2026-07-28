# Configuration Guide - flext-web

<!-- TOC START -->
- [Canonical Access](#canonical-access)
- [Settings Model](#settings-model)
- [Validation](#validation)
- [Environment Variables](#environment-variables)
- [Service Bootstrap](#service-bootstrap)
- [Operational Rules](#operational-rules)
<!-- TOC END -->

`flext-web` exposes its validated singleton directly through the package root:

```python
from flext_web import settings

host = settings.Web.host
```

## Canonical Access

Use `settings.Web` for live values and construct `FlextWebSettings` at an
external boundary when explicit validated overrides are required.

```python
from flext_web import FlextWebSettings, u

runtime_settings = FlextWebSettings(Web={"host": "127.0.0.1", "port": 8080}, debug=True)
assert u.Web.validate_settings(runtime_settings).unwrap()
assert (
    u.Web.base_url(
        host=runtime_settings.Web.host,
        port=runtime_settings.Web.port,
        ssl_enabled=runtime_settings.Web.ssl_enabled,
    )
    == "http://127.0.0.1:8080"
)
```

## Settings Model

The canonical model is `FlextWebSettings(FlextSettings)` and it is registered
under the namespace `settings.Web`.

Primary fields:

- `app_name`
- `host`
- `port`
- `testing`
- `secret_key`
- `ssl_enabled`
- `ssl_cert_path`
- `ssl_key_path`

Universal fields such as `debug` remain on the settings root. Derived values
are computed by `u.Web`:

- `protocol`
- `base_url`

## Validation

`flext-web` validates host, port, secret key and optional TLS paths through the
settings model itself.

```python
from flext_web import FlextWebSettings, u

runtime_settings = FlextWebSettings(
    Web={
        "host": "localhost",
        "port": 8080,
        "secret_key": "development-secret-key-32-characters-long",
    }
)
assert u.Web.validate_settings(runtime_settings).unwrap()
```

Invalid values fail during boundary validation:

```python
from pydantic import ValidationError

from flext_web import FlextWebSettings

try:
    FlextWebSettings(Web={"host": "", "port": -1})
except ValidationError:
    pass
else:
    raise AssertionError("invalid web settings must fail validation")
```

## Environment Variables

The settings namespace follows the `FLEXT_WEB_` environment prefix inherited
from `FlextSettings`.

Common variables:

- `FLEXT_WEB_WEB__APP_NAME`
- `FLEXT_WEB_WEB__HOST`
- `FLEXT_WEB_WEB__PORT`
- `FLEXT_WEB_DEBUG`
- `FLEXT_WEB_WEB__SECRET_KEY`
- `FLEXT_WEB_WEB__SSL_ENABLED`
- `FLEXT_WEB_WEB__SSL_CERT_PATH`
- `FLEXT_WEB_WEB__SSL_KEY_PATH`

## Service Bootstrap

Configuration and lifecycle stay on the public facade:

```python
from flext_web import FlextWebSettings, web

runtime_settings = FlextWebSettings(
    Web={
        "host": "0.0.0.0",
        "port": 8080,
        "secret_key": "production-secret-key-32-characters-long",
    },
    debug=False,
)

start_result = web.start_service(
    host=runtime_settings.Web.host,
    port=runtime_settings.Web.port,
    debug=runtime_settings.debug,
)
assert start_result.success
```

## Operational Rules

- Do not create parallel settings helpers outside `FlextWebSettings`.
- Do not use obsolete helpers such as `get_web_settings`, `reset_web_settings`
  or `validate_config`.
- Read the direct `settings.Web` singleton and validate explicit overrides with
  `FlextWebSettings`.
