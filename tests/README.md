# flext-web tests

The test suite is anchored on the canonical public surface:

```python
from flext_web import web, c, t, p, m, u
```

## Current structure

```text
tests/
├── conftest.py
├── integration/
│   └── test_examples.py
├── unit/
│   ├── test___init__.py
│   ├── test___main__.py
│   ├── test_api.py
│   ├── test_app.py
│   ├── test_config.py
│   ├── test_handlers.py
│   ├── test_models.py
│   ├── test_protocols.py
│   └── test_services.py
├── constants.py
├── models.py
├── protocols.py
├── typings.py
└── utilities.py
```

## Rules

- Test code should import runtime operations through `web`.
- Structural assertions should use the canonical aliases `c`, `t`, `p`, `m`, `u`.
- Integration tests must validate real public usage, not dead HTTP contracts or private internals.

## Running

```bash
make test
make test FILE=tests/unit/test___init__.py
make test FILE=tests/integration/test_examples.py
make check
make check FILES="src/flext_web/api.py tests/unit/test___init__.py"
```

## What is validated

- `web` exposes the full public service surface by MRO composition.
- `c.Web`, `t.Web`, `p.Web`, `m.Web`, and `u.Web` remain available as SSOT namespaces.
- Examples stay aligned with the public facade instead of reintroducing parallel APIs.
