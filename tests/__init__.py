"""FLEXT Web Tests - Test infrastructure and utilities.

Provides TestsFlextWeb classes extending FlextTests and FlextWeb for comprehensive testing.
Centralized runtime aliases: c, p, m, r, t, u, s from tests and flext_web.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from flext_core import r
from flext_web import (
    FlextWebApi,
    FlextWebApp,
    FlextWebHandlers,
    FlextWebServices,
    FlextWebSettings,
    _ApplicationConfig,
    _WebRequestConfig,
    _WebResponseConfig,
)

from tests.constants import TestsFlextWebConstants, c
from tests.models import TestsFlextWebModels, m
from tests.protocols import TestsFlextWebProtocols, p
from tests.typings import TestsFlextWebTypes, t
from tests.utilities import TestsFlextWebUtilities, u

# Service alias per FLEXT convention
s = FlextWebServices

__all__ = [
    "FlextWebApi",
    "FlextWebApp",
    "FlextWebHandlers",
    "FlextWebServices",
    "FlextWebSettings",
    "TestsFlextWebConstants",
    "TestsFlextWebModels",
    "TestsFlextWebProtocols",
    "TestsFlextWebTypes",
    "TestsFlextWebUtilities",
    "_ApplicationConfig",
    "_WebRequestConfig",
    "_WebResponseConfig",
    "c",
    "m",
    "p",
    "r",
    "s",
    "t",
    "u",
]
