# FLEXT Web - Usage Examples

This directory shows the current public usage pattern for `flext-web`:
`from flext_web import web, c, t, p, m, u`.

## Basic Usage

```python
from flext_web import web

config = web.settings.create_web_config(host="127.0.0.1", port=8000, debug=True).value
_ = web.start_service(host=config.host, port=config.port, debug=config.debug_mode)
```

## API Usage

```python
from flext_web import m, web

created = web.create_app(m.Web.AppData(name="demo", host="127.0.0.1", port=8080))
assert created.is_success
started = web.start_app(created.value.id)
assert started.is_success
```

## Flask Integration

```python
from flask import Flask
from flext_web import web

app_result = web.create_flask_app()
assert app_result.is_success
app: Flask = app_result.value
```

## Testing

```python
from flext_web import web

assert web.get_service_status().is_success
assert web.get_api_capabilities().is_success
```

## Running The Examples

```bash
cd examples
python 01_basic_service.py
python 02_api_usage.py
```
