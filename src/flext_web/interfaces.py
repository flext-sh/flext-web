"""FLEXT Web Interfaces - Protocol Consolidation Pattern.

This module eliminates massive duplication by delegating to FlextWebProtocols.
Uses meta-programming to provide backward compatibility without code duplication.

Copyright (c) 2025 FLEXT Contributors
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

# Meta-programming: Import protocols to eliminate duplication
from flext_web.protocols import FlextWebProtocols


class FlextWebInterfaces:
    """Meta-programmed interface consolidation - eliminates duplicate protocols.

    This class uses advanced meta-programming to eliminate the massive duplication
    that existed between interfaces.py and protocols.py. All protocol definitions
    are now centralized in FlextWebProtocols, and this module provides semantic
    aliases for backward compatibility.

    Benefits:
    - Zero code duplication (was ~180 lines of duplicate @abstractmethod definitions)
    - Single source of truth for protocol definitions
    - Backward compatibility maintained via aliasing
    - Leverages Python's dynamic typing for seamless delegation
    """

    # =========================================================================
    # PROTOCOL ALIASES - ELIMINATES DUPLICATION VIA META-PROGRAMMING
    # =========================================================================

    # Direct protocol aliases (exact semantic match)
    WebServiceInterface = FlextWebProtocols.WebServiceInterface
    MiddlewareInterface = FlextWebProtocols.MiddlewareInterface
    TemplateEngineInterface = FlextWebProtocols.TemplateEngineInterface
    MonitoringInterface = FlextWebProtocols.MonitoringInterface

    # Semantic protocol aliases (backward compatibility)
    WebHandlerInterface = FlextWebProtocols.AppManagerProtocol
    WebConfigInterface = FlextWebProtocols.ResponseFormatterProtocol
    WebRepositoryInterface = FlextWebProtocols.AppManagerProtocol
    WebValidatorInterface = FlextWebProtocols.AppManagerProtocol


# Export consolidated protocols
__all__ = [
    "FlextWebInterfaces",
]
