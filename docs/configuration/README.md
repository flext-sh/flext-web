# Configuration Guide - flext-web

<!-- TOC START -->
- [Canonical Access](#canonical-access)
- [Settings Model](#settings-model)
- [Validation](#validation)
- [Environment Variables](#environment-variables)
- [Service Bootstrap](#service-bootstrap)
- [Operational Rules](#operational-rules)
<!-- TOC END -->

`flext-web` exposes configuration through the registered namespace on the
public facade:

```python
from flext_web import web

settings = web.settings
```

## Canonical Access

Use `web.settings` for the live namespaced settings instance and
`web.settings.create_web_config(...)` when you need validated overrides.

```python
from flext_web import web

config_result = web.settings.create_web_config(
    host="127.0.0.1",
    port=8080,
    debug=True,
)
assert config_result.success

settings = config_result.value
assert settings.base_url == "http://127.0.0.1:8080"
```

## Settings Model

The canonical model is `FlextWebSettings(FlextSettings)` and it is registered
under the namespace `web`.

Primary fields:

- `app_name`
- `host`
- `port`
- `debug_mode`
- `debug`
- `testing`
- `secret_key`
- `ssl_enabled`
- `ssl_cert_path`
- `ssl_key_path`

Computed fields:

- `protocol`
- `base_url`

## Validation

`flext-web` validates host, port, secret key and optional TLS paths through the
settings model itself.

```python
from flext_web import web

config_result = web.settings.create_web_config(
    host="localhost",
    port=8080,
    secret_key="development-secret-key-32-characters-long",
)
assert config_result.success

validation_result = web.settings.validate_settings(config_result.value)
assert validation_result.success
```

Invalid values fail through `r[...]`:

```python
from flext_web import web

result = web.settings.create_web_config(host="", port=-1)
assert result.failure
```

## Environment Variables

The settings namespace follows the `FLEXT_WEB_` environment prefix inherited
from `FlextSettings`.

Common variables:

- `FLEXT_WEB_APP_NAME`
- `FLEXT_WEB_HOST`
- `FLEXT_WEB_PORT`
- `FLEXT_WEB_DEBUG`
- `FLEXT_WEB_SECRET_KEY`
- `FLEXT_WEB_SSL_ENABLED`
- `FLEXT_WEB_SSL_CERT_PATH`
- `FLEXT_WEB_SSL_KEY_PATH`

## Service Bootstrap

Configuration and lifecycle stay on the public facade:

```python
from flext_web import web

config_result = web.settings.create_web_config(
    host="0.0.0.0",
    port=8080,
    debug=False,
    secret_key="production-secret-key-32-characters-long",
)
assert config_result.success

start_result = web.start_service(
    host=config_result.value.host,
    port=config_result.value.port,
    debug=config_result.value.debug_mode,
)
assert start_result.success
```

## Operational Rules

- Do not create parallel settings helpers outside `FlextWebSettings`.
- Do not use obsolete helpers such as `get_web_settings`, `reset_web_settings`
  or `validate_config`.
- Prefer `web.settings` for reads and `create_web_config` for validated
  overrides.
