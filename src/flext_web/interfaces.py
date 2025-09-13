"""FLEXT Web Interfaces - Protocol Consolidation Pattern.

Uses meta-programming to provide backward compatibility without code duplication.

Copyright (c) 2025 FLEXT Contributors
SPDX-License-Identifier: MIT
"""

from __future__ import annotations


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

    # Use FlextWebProtocols.WebServiceInterface instead of WebServiceInterface
    # Use FlextWebProtocols.MiddlewareInterface instead of MiddlewareInterface
    # Use FlextWebProtocols.TemplateEngineInterface instead of TemplateEngineInterface
    # Use FlextWebProtocols.MonitoringInterface instead of MonitoringInterface
    # Use FlextWebProtocols.AppManagerProtocol directly for app management
    # Use FlextWebProtocols.ResponseFormatterProtocol directly for responses


# Export consolidated protocols
__all__ = [
    "FlextWebInterfaces",
]
