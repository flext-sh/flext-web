"""Copyright (c) 2025 FLEXT Team. All rights reserved.

SPDX-License-Identifier: MIT.
"""

from __future__ import annotations

from typing import Final

from flext_web.app import FlextWebApp, create_fastapi_app
from flext_web.config import FlextWebConfig
from flext_web.constants import FlextWebConstants
from flext_web.exceptions import FlextWebExceptions
from flext_web.fields import FlextWebFields
from flext_web.handlers import FlextWebHandlers
from flext_web.models import FlextWebModels
from flext_web.protocols import FlextWebProtocols
from flext_web.services import FlextWebServices
from flext_web.typings import FlextWebTypes
from flext_web.utilities import FlextWebUtilities
from flext_web.version import VERSION, FlextWebVersion

PROJECT_VERSION: Final[FlextWebVersion] = VERSION

__version__: str = VERSION.version
__version_info__: tuple[int | str, ...] = VERSION.version_info

__all__ = [
    "PROJECT_VERSION",
    "VERSION",
    "FlextWebApp",
    "FlextWebConfig",
    "FlextWebConstants",
    "FlextWebExceptions",
    "FlextWebFields",
    "FlextWebHandlers",
    "FlextWebModels",
    "FlextWebProtocols",
    "FlextWebServices",
    "FlextWebTypes",
    "FlextWebUtilities",
    "FlextWebVersion",
    "__version__",
    "__version_info__",
    "create_fastapi_app",
]
