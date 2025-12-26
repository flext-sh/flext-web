"""FLEXT Web framework integration.

Provides web framework integration and HTTP handling for FLEXT applications.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from flext_web.__version__ import __version__, __version_info__
from flext_web.api import FlextWebApi
from flext_web.app import FlextWebApp
from flext_web.constants import FlextWebConstants, c
from flext_web.handlers import FlextWebHandlers
from flext_web.models import FlextWebModels, m
from flext_web.protocols import FlextWebProtocols, p
from flext_web.services import FlextWebServices
from flext_web.settings import FlextWebSettings
from flext_web.typings import FlextWebTypes, t
from flext_web.utilities import FlextWebUtilities, u

__all__ = [
    "FlextWebApi",
    "FlextWebApp",
    "FlextWebConstants",
    "FlextWebHandlers",
    "FlextWebModels",
    "FlextWebProtocols",
    "FlextWebServices",
    "FlextWebSettings",
    "FlextWebTypes",
    "FlextWebUtilities",
    "__version__",
    "__version_info__",
    "c",
    "m",
    "p",
    "t",
    "u",
]
