"""Copyright (c) 2025 FLEXT Team. All rights reserved.

SPDX-License-Identifier: MIT.
"""

from __future__ import annotations

from flext_web.config import FlextWebConfigs
from flext_web.constants import FlextWebConstants
from flext_web.exceptions import FlextWebExceptions
from flext_web.fields import FlextWebFields
from flext_web.handlers import FlextWebHandlers
from flext_web.interfaces import FlextWebInterfaces
from flext_web.models import FlextWebModels
from flext_web.protocols import FlextWebProtocols
from flext_web.services import FlextWebServices
from flext_web.settings import FlextWebSettings
from flext_web.typings import FlextTypes, FlextWebTypes
from flext_web.utilities import FlextWebUtilities

__version__ = "0.9.0"

__all__ = [
    "FlextTypes",
    "FlextWebConfigs",
    "FlextWebConstants",
    "FlextWebExceptions",
    "FlextWebFields",
    "FlextWebHandlers",
    "FlextWebInterfaces",
    "FlextWebModels",
    "FlextWebProtocols",
    "FlextWebServices",
    "FlextWebSettings",
    "FlextWebTypes",
    "FlextWebUtilities",
]
