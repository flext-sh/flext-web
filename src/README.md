# flext-web source

`src/flext_web` is organized around one public operational facade and five
public structural namespaces:

```python
from flext_web import web, c, t, p, m, u
```

## Public contract

- `web`: operational entrypoint for runtime, app lifecycle, auth, entities, health, handlers, and framework factories.
- `c.Web`: constants and enums.
- `t.Web`: public type contracts.
- `u.Web`: public protocol contracts and runtime registries.
- `m.Web`: public models and response projections.
- `u.Web`: public utilities.

## Key modules

```text
src/flext_web/
├── api.py              # public facade composed from all service classes
├── base.py             # shared service base with typed web settings access
├── settings.py         # registered web settings namespace
├── services/
│   ├── app.py          # FastAPI/Flask factories
│   ├── auth.py         # auth operations
│   ├── entities.py     # entity CRUD support
│   ├── handlers.py     # handler-oriented projections exposed by the facade
│   ├── health.py       # health and metrics operations
│   └── web.py          # canonical service orchestration
├── protocols.py        # runtime protocol and registry behavior
├── models.py           # public models and projections
├── typings.py          # public type layer
├── constants.py        # public constants
└── utilities.py        # public utilities
```

## Usage rule

- Consumers should not import internal service modules for normal operations.
- If an operation is public, it should be reachable through `web`.
- If a contract is public, it should live under `.Web` in `c`, `t`, `p`, `m`, or `u`.
