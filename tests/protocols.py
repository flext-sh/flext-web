"""Test protocol definitions for flext-web.

Provides TestsFlextWebProtocols, combining FlextTestsProtocols with
FlextWebProtocols for test-specific protocol definitions.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from flext_tests import FlextTestsProtocols
from flext_web import FlextWebProtocols


class TestsFlextWebProtocols(FlextTestsProtocols, FlextWebProtocols):
    """Test protocols combining FlextTestsProtocols and FlextWebProtocols.

    Provides access to:
    - p.Tests.Docker.* (from FlextTestsProtocols)
    - p.Tests.Factory.* (from FlextTestsProtocols)
    - p.Web.* (from FlextWebProtocols)
    """

    class Web(FlextWebProtocols.Web):
        """Web-specific test protocols."""

        class Tests:
            """Project-specific test protocols.

            Extends Tests Web-specific protocols.
            """


# Runtime aliases per FLEXT convention
p = TestsFlextWebProtocols

__all__ = ["TestsFlextWebProtocols", "p"]
