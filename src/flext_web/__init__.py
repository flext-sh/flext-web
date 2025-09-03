"""FLEXT Web - Enterprise Web Management Console for FLEXT ecosystem.

Single consolidated web interface providing management dashboard and REST API
following flext-core architectural patterns with wildcard imports aggregation.

Copyright (c) 2025 FLEXT Contributors
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

# =============================================================================
# FOUNDATION LAYER - Import first, no dependencies on other modules
# =============================================================================

from flext_web.__version__ import *
from flext_web.constants import *
from flext_web.typings import *
from flext_web.exceptions import *
from flext_web.protocols import *

# =============================================================================
# DOMAIN LAYER - Depends only on Foundation layer
# =============================================================================

from flext_web.models import *

# =============================================================================
# APPLICATION LAYER - Depends on Domain + Foundation layers
# =============================================================================

from flext_web.handlers import *
from flext_web.fields import *

# =============================================================================
# INFRASTRUCTURE LAYER - Depends on Application + Domain + Foundation
# =============================================================================

from flext_web.config import *  # type: ignore[assignment]
from flext_web.services import *  # type: ignore[assignment]

# =============================================================================
# SUPPORT LAYER - Depends on layers as needed, imported last
# =============================================================================

from flext_web.utilities import *

# =============================================================================
# CONSOLIDATED EXPORTS - Combine all __all__ from modules
# =============================================================================

# Collect all __all__ exports from imported modules (following flext-core pattern)
import flext_web.__version__ as _version
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

_temp_exports: list[str] = []

for module in [
    _version,
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
# Version is now included via _version module - no manual addition needed
_final_exports.sort()

# Define __all__ as literal list for linter compatibility
# This dynamic assignment is necessary for aggregating module exports
__all__: list[str] = _final_exports  # noqa: PLE0605 # type: ignore[reportUnsupportedDunderAll]
