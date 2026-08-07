# Triagem Snyk Code (SAST) — flext-sh/flext-web

Gerado do scan Snyk da org Datacosmos (dump 2026-08-06).

**6 achados** — critical 0, high 1, medium 0, low 5

| categoria | achados |
|---|---|
| Hardcoded Non-Cryptographic Secret | 6 |

## Achados

Coluna **Decisão**: `corrigir` / `falso-positivo` / `risco-aceito`.

| # | sev | categoria | arquivo | linha | CWE | Decisão |
|---|---|---|---|---|---|---|
| 1 | high | Hardcoded Non-Cryptographic Secret | `examples/01_basic_service.py` | 15 | - | |
| 2 | low | Hardcoded Non-Cryptographic Secret | `tests/conftest.py` | 57 | - | |
| 3 | low | Hardcoded Non-Cryptographic Secret | `tests/unit/test_api.py` | 53 | - | |
| 4 | low | Hardcoded Non-Cryptographic Secret | `tests/unit/test_app.py` | 26 | - | |
| 5 | low | Hardcoded Non-Cryptographic Secret | `tests/unit/test_config.py` | 64 | - | |
| 6 | low | Hardcoded Non-Cryptographic Secret | `tests/unit/test_fields.py` | 49 | - | |

## Como triar

1. Abrir `arquivo:linha` e seguir o fluxo de dados até o sink.
2. Classificar: **corrigir** (entrada externa alcança o sink sem sanitização), **falso-positivo** (credencial de fixture, path de constante — registrar em `.snyk` com justificativa), **risco-aceito** (com prazo de revisão).

Dados brutos: `~/snyk-violations/sast/flext-sh__flext-web.sast.json`

