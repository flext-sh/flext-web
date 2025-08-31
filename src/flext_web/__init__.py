"""FLEXT Web - Enterprise Web Management Console for FLEXT ecosystem.

Single consolidated web interface providing management dashboard and REST API
following flext-core architectural patterns with wildcard imports aggregation.

Copyright (c) 2025 FLEXT Contributors
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

# Version information
__version__ = "0.9.0"

# =============================================================================
# FOUNDATION LAYER - Import first, no dependencies on other modules
# =============================================================================

from flext_web.constants import *  # type: ignore[unused-ignore,reportWildcardImport,assignment] # noqa: F403
from flext_web.typings import *  # type: ignore[unused-ignore,reportWildcardImport,assignment] # noqa: F403
from flext_web.exceptions import *  # type: ignore[unused-ignore,reportWildcardImport,assignment] # noqa: F403
from flext_web.protocols import *  # type: ignore[unused-ignore,reportWildcardImport,assignment] # noqa: F403

# =============================================================================
# DOMAIN LAYER - Depends only on Foundation layer
# =============================================================================

from flext_web.models import *  # type: ignore[unused-ignore,reportWildcardImport,assignment] # noqa: F403

# =============================================================================
# APPLICATION LAYER - Depends on Domain + Foundation layers
# =============================================================================

from flext_web.handlers import *  # type: ignore[unused-ignore,reportWildcardImport,assignment] # noqa: F403
from flext_web.fields import *  # type: ignore[unused-ignore,reportWildcardImport,assignment] # noqa: F403

# =============================================================================
# INFRASTRUCTURE LAYER - Depends on Application + Domain + Foundation
# =============================================================================

from flext_web.config import *  # type: ignore[unused-ignore,reportWildcardImport,assignment] # noqa: F403
from flext_web.services import *  # type: ignore[unused-ignore,reportWildcardImport,assignment] # noqa: F403

# =============================================================================
# SUPPORT LAYER - Depends on layers as needed, imported last
# =============================================================================

from flext_web.utilities import *  # type: ignore[unused-ignore,reportWildcardImport,assignment] # noqa: F403

# Import factory functions for convenience
from flext_web.config import FlextWebConfigs
from flext_web.services import FlextWebServices

# Convenience factory functions
create_service = FlextWebServices.create_web_service
create_web_config = FlextWebConfigs.create_web_config

# Import aliases for backward compatibility and test fixes
FlextWebService = FlextWebServices.WebService

# =============================================================================
# CONSOLIDATED EXPORTS - Combine all __all__ from modules
# =============================================================================

# Combine all __all__ exports from imported modules
import flext_web.config as _config
import flext_web.constants as _constants
import flext_web.exceptions as _exceptions
import flext_web.fields as _fields
import flext_web.handlers as _handlers
import flext_web.models as _models
import flext_web.protocols as _protocols
import flext_web.services as _services
import flext_web.typings as _typings
import flext_web.utilities as _utilities

# Collect all __all__ exports from imported modules
_temp_exports: list[str] = []

for module in [
    _constants,
    _typings,
    _exceptions,
    _protocols,
    _models,
    _fields,
    _handlers,
    _config,
    _services,
    _utilities,
]:
    if hasattr(module, "__all__"):
        _temp_exports.extend(module.__all__)

# Remove duplicates and sort for consistent exports - build complete list first
_seen: set[str] = set()
_final_exports: list[str] = []
for item in _temp_exports:
    if item not in _seen:
        _seen.add(item)
        _final_exports.append(item)
# Add compatibility aliases and factory functions to exports
_final_exports.extend(["FlextWebService", "create_service", "create_web_config", "__version__"])
_final_exports.sort()

# Define __all__ as literal list for linter compatibility
# This dynamic assignment is necessary for aggregating module exports
__all__: list[str] = _final_exports  # pyright: ignore[reportUnsupportedDunderAll] # noqa: PLE0605
