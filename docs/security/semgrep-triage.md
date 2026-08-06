# Triagem Semgrep — flext-sh/flext-web

Gerado do dump da plataforma Semgrep (deployment `datacosmos`, 2026-08-06).

Bead de rastreio: `mro-p57t.32`

## Resumo

**5 findings** — high 0, medium 5, low 0
Confiança: high 4, medium 0, low 1

| regra | achados |
|---|---|
| `package_managers.dependabot.dependabot-missing-cooldown.dependabot-missing-cooldown` | 3 |
| `package_managers.uv.uv-missing-dependency-cooldown.uv-missing-dependency-cooldown` | 1 |
| `python.flask.security.audit.hardcoded-config.avoid_hardcoded_config_TESTING` | 1 |

## Findings

Coluna **Decisão** a preencher: `corrigir` / `falso-positivo` / `risco-aceito`.

| # | sev | conf | regra | arquivo | linha | Decisão |
|---|---|---|---|---|---|---|
| 1 | medium | high | `dependabot-missing-cooldown` | `.github/dependabot.yml` | 4 | |
| 2 | medium | high | `dependabot-missing-cooldown` | `.github/dependabot.yml` | 11 | |
| 3 | medium | high | `dependabot-missing-cooldown` | `.github/dependabot.yml` | 18 | |
| 4 | medium | high | `uv-missing-dependency-cooldown` | `pyproject.toml` | 610 | |
| 5 | medium | low | `avoid_hardcoded_config_TESTING` | `src/flext_web/utilities.py` | 140 | |

## Como triar

1. Abrir `arquivo:linha` e seguir o fluxo até o sink.
2. Classificar: **corrigir** (entrada externa alcança o sink), **falso-positivo** (registrar via `nosemgrep` ou `.semgrepignore` com justificativa), **risco-aceito** (com prazo de revisão).
3. Priorizar findings high com confidence=high.

Dados brutos: `~/semgrep-violations/by-repo/flext-sh__flext-web.json`

