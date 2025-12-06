"""Copyright (c) 2025 FLEXT Team. All rights reserved.

SPDX-License-Identifier: MIT.
"""

from __future__ import annotations

from flext_core import (
    FlextDecorators,
    FlextExceptions,
    FlextHandlers,
    FlextMixins,
    FlextResult,
    FlextService,
)

from flext_web.__version__ import __version__, __version_info__
from flext_web.api import FlextWebApi
from flext_web.app import FlextWebApp
from flext_web.config import FlextWebConfig
from flext_web.constants import FlextWebConstants
from flext_web.handlers import FlextWebHandlers
from flext_web.models import FlextWebModels
from flext_web.protocols import FlextWebProtocols
from flext_web.services import FlextWebServices
from flext_web.typings import FlextWebTypes
from flext_web.utilities import FlextWebUtilities

# Domain-specific aliases (extending flext-core base classes)
u = FlextWebUtilities  # Utilities (FlextWebUtilities extends FlextUtilities)
m = FlextWebModels  # Models (FlextWebModels extends FlextModels)
c = FlextWebConstants  # Constants (FlextWebConstants extends FlextConstants)
t = FlextWebTypes  # Types (FlextWebTypes extends FlextTypes)
p = FlextWebProtocols  # Protocols (FlextWebProtocols extends FlextProtocols)
r = FlextResult  # Shared from flext-core
e = FlextExceptions  # Shared from flext-core
d = FlextDecorators  # Shared from flext-core
s = FlextService  # Shared from flext-core
x = FlextMixins  # Shared from flext-core
h = FlextHandlers  # Shared from flext-core

__all__ = [
    "FlextWebApi",
    "FlextWebApp",
    "FlextWebConfig",
    "FlextWebConstants",
    "FlextWebHandlers",
    "FlextWebModels",
    "FlextWebProtocols",
    "FlextWebServices",
    "FlextWebTypes",
    "FlextWebUtilities",
    "__version__",
    "__version_info__",
    # Domain-specific aliases
    "c",
    # Global aliases
    "d",
    "e",
    "h",
    "m",
    "p",
    "r",
    "s",
    "t",
    "u",
    "x",
]
