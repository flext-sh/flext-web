"""Copyright (c) 2025 FLEXT Team. All rights reserved.

SPDX-License-Identifier: MIT.
"""

from __future__ import annotations

from flext_web.__version__ import __version__, __version_info__
from flext_web.api import FlextWeb
from flext_web.app import FlextWebApp
from flext_web.config import FlextWebConfig
from flext_web.constants import FlextWebConstants
from flext_web.fields import FlextWebFields
from flext_web.handlers import FlextWebHandlers
from flext_web.models import FlextWebModels
from flext_web.services import FlextWebService
from flext_web.typings import FlextWebTypes
from flext_web.utilities import FlextWebUtilities

__all__ = [
    "FlextWeb",
    "FlextWebApp",
    "FlextWebConfig",
    "FlextWebConstants",
    "FlextWebFields",
    "FlextWebHandlers",
    "FlextWebModels",
    "FlextWebService",
    "FlextWebTypes",
    "FlextWebUtilities",
    "__version__",
    "__version_info__",
]
