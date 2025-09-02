"""FLEXT Web Constants - Domain-specific constants (eliminando duplicações com flext-core).

ZERO DUPLICAÇÃO: Usa APENAS FlextConstants de flext-core para tudo genérico.
Define SOMENTE constantes específicas do domínio web que não existem em flext-core.

Copyright (c) 2025 FLEXT Contributors
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

import os

from flext_core import FlextConstants


class FlextWebConstants(FlextConstants):
    """Web domain-specific constants - APENAS extensões necessárias.

    ZERO DUPLICAÇÃO: Herda TUDO de FlextConstants e adiciona APENAS
    constantes específicas do domínio web que não podem ser genéricas.

    Usar FlextConstants.Web.* para tudo que já existe lá!
    """

    class WebSpecific:
        """Constantes ESPECÍFICAS do domínio flext-web (não genéricas)."""

        # Environment variable específica do flext-web
        ENV_SECRET_KEY = "FLEXT_WEB_SECRET_KEY"
        ENV_HOST = "FLEXT_WEB_HOST"
        ENV_PORT = "FLEXT_WEB_PORT"
        ENV_DEBUG = "FLEXT_WEB_DEBUG"

        # Default secret key com valor específico flext-web
        DEFAULT_SECRET_KEY = os.getenv(
            ENV_SECRET_KEY, "dev-secret-key-change-in-production"
        )

        # Port threshold for system ports (web-specific business rule)
        SYSTEM_PORTS_THRESHOLD = 1024

        # Network port validation constants
        MIN_PORT = 1
        MAX_PORT = 65535

        # Security validation constants
        MIN_SECRET_KEY_LENGTH = 32

        # Development/test keys (properly marked for security scanners)
        DEV_SECRET_KEY = "dev-key-change-in-production-32chars!"
        DEV_ENVIRONMENT_KEY = "dev-key-for-development-environment!"
        TEST_ENVIRONMENT_KEY = "test-key-for-testing-environment!"


__all__ = [
    "FlextWebConstants",
]
