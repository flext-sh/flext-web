"""Test protocol definitions for flext-web.

Provides TestsFlextWebProtocols, combining FlextTestsProtocols with
FlextWebProtocols for test-specific protocol definitions.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from flext_tests.protocols import FlextTestsProtocols
from flext_web.protocols import FlextWebProtocols


class TestsFlextWebProtocols(FlextTestsProtocols, FlextWebProtocols):
    """Test protocols combining FlextTestsProtocols and FlextWebProtocols.

    Provides access to:
    - p.Tests.Docker.* (from FlextTestsProtocols)
    - p.Tests.Factory.* (from FlextTestsProtocols)
    - p.Web.* (from FlextWebProtocols)
    """

    class Tests:
        """Project-specific test protocols.

        Extends FlextTestsProtocols.Tests with Web-specific protocols.
        """

        class Web:
            """Web-specific test protocols."""


# Runtime aliases
p = TestsFlextWebProtocols
p = TestsFlextWebProtocols

__all__ = ["TestsFlextWebProtocols", "p"]
