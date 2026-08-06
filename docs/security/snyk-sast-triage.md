# Triagem Snyk Code (SAST) — flext-sh/flext-web

Gerado do scan Snyk (dump 2026-08-06). Bead: `mro-kcx5`

## Resumo

**6 achados** — critical 0, high 1, medium 0, low 5

| categoria | achados |
|---|---|
| Hardcoded Non-Cryptographic Secret | 6 |

## Como usar este documento

Cada achado traz o **código real** extraído da worktree (linha `>>>` = sink reportado), a regra completa e o CWE.
Preencha **Decisão**: `corrigir` / `falso-positivo` (registrar em `.snyk`) / `risco-aceito` (com prazo).

## Achados

### 1 · 🟠 HIGH · Hardcoded Non-Cryptographic Secret
**Local**: `examples/01_basic_service.py:15` · **CWE**: -

```python
       11      settings = web.settings.clone(
       12          Web={
       13              "host": "127.0.0.1",
       14              "port": 8000,
>>>    15              "secret_key": "dev-secret-key-32-characters-long",
       16          },
       17          debug=True,
       18      )
       19      try:
```

**Decisão**: 

### 2 · ⚪ LOW · Hardcoded Non-Cryptographic Secret
**Local**: `tests/conftest.py:57` · **CWE**: -

```python
       53          "FLEXT_ENV": "test",
       54          "FLEXT_LOG_LEVEL": "INFO",
       55          "FLEXT_WEB_DEBUG_MODE": "true",
       56          "FLEXT_WEB_WEB__HOST": "localhost",
>>>    57          "FLEXT_WEB_WEB__SECRET_KEY": "test-secret-key-32-characters-long-for-tests",
       58          "FLEXT_WEB_WEB__AUTH_USERNAME": "testuser",
       59          "FLEXT_WEB_WEB__AUTH_PASSWORD": "test-password-from-environment",
       60      }):
       61          yield
```

**Decisão**: 

### 3 · ⚪ LOW · Hardcoded Non-Cryptographic Secret
**Local**: `tests/unit/test_api.py:53` · **CWE**: -

```python
       49          settings = web.settings.clone(
       50              Web={
       51                  "host": "localhost",
       52                  "port": 8080,
>>>    53                  "secret_key": "test-secret-key-32-characters!!!",
       54              },
       55              debug=True,
       56          )
       57          validated = type(settings).model_validate(settings.model_dump())
```

**Decisão**: 

### 4 · ⚪ LOW · Hardcoded Non-Cryptographic Secret
**Local**: `tests/unit/test_app.py:26` · **CWE**: -

```python
       22              Web={
       23                  "app_name": "flext-web-test",
       24                  "host": "127.0.0.1",
       25                  "port": 8123,
>>>    26                  "secret_key": "flask-secret-key-32-characters!!",
       27              },
       28              debug=True,
       29          )
       30          result = web.create_flask_app(settings)
```

**Decisão**: 

### 5 · ⚪ LOW · Hardcoded Non-Cryptographic Secret
**Local**: `tests/unit/test_config.py:64` · **CWE**: -

```python
       60  
       61      def test_validation_secret_key_valid(self) -> None:
       62          """Valid secret keys are accepted by namespaced validation."""
       63          settings = web.settings.clone(
>>>    64              Web={"secret_key": "valid-secret-key-32-characters-long"}
       65          )
       66          tm.that(settings.Web.secret_key, none=False)
       67  
       68      def test_ssl_configuration_valid(self) -> None:
```

**Decisão**: 

### 6 · ⚪ LOW · Hardcoded Non-Cryptographic Secret
**Local**: `tests/unit/test_fields.py:49` · **CWE**: -

```python
       45  
       46      def test_secret_key_field_creation(self) -> None:
       47          """Test secret key field creation."""
       48          settings = web.settings.clone(
>>>    49              Web={"secret_key": "valid-secret-key-32-characters-long"}
       50          )
       51          tm.that(settings.Web.secret_key, none=False)
       52  
       53      def test_http_status_field_creation(self) -> None:
```

**Decisão**: 

