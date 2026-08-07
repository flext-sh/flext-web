# AGENTS.md — flext-web

> **Parent workspace law** lives in [`../AGENTS.md`](../AGENTS.md) — read it first.
> Universal engineering core: `~/.agents/UNIVERSAL_CORE.md`. Composition: global skills + parent/root `AGENTS.md` + this scope delta. Do not re-embed universal law.
>
> **Standalone / independent mode:** when `../AGENTS.md` does not resolve, pin the parent raw `AGENTS.md` URL to the same branch/release as this package (never `main`).

<!-- AIHUB-AGENTS-SCOPE-LOCAL-BEGIN -->
**Package:** `flext_web` · deps: `flext-cli`, `flext-core`

## Overview

Modern web interface for the FLEXT platform.

## Structure

```text
src/flext_web/
├── api.py __main__.py    # FlextWeb facade (inherits FlextService)
├── base.py utilities.py
├── services/
├── constants.py typings.py protocols.py models.py               # AUTO-GENERATED facets
└── _settings.py _models/ _protocols/
```

## Code Map

| Symbol | Kind | Location | Role |
|--------|------|----------|------|
| `FlextWeb` | class | `api.py` | facade; inherits `FlextService` → `FlextWeb.fetch_global()` |

## Conventions (specific to this package)

- Keep web behavior in the service/facade layer; treat generated declaration facets as data-only.
- Response payloads typed via `t.Web.*` aliases (never raw dict / `m.Dict`); `_start_app_runtime` narrows the interface via `isinstance` guards.
- Config/settings canonical pattern: ADR-012.
- Codemod governance (ast-grep + make mod): ADR-014.

## Commands

```bash
make check PROJECT=flext-web
make test  PROJECT=flext-web       # tests/{unit,integration}
```
<!-- AIHUB-AGENTS-SCOPE-LOCAL-END -->
