"""Test protocols for flext-web.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from flext_tests import FlextTestsProtocols

from flext_web import FlextWebProtocols


class FlextWebTestProtocols(FlextTestsProtocols, FlextWebProtocols):
    """Test protocols for flext-web."""

    class Web(FlextWebProtocols.Web):
        """Web domain test protocols."""

        class Tests:
            """Test-specific protocols."""


p = FlextWebTestProtocols
__all__ = ["FlextWebTestProtocols", "p"]
