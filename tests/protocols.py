"""Test protocol definitions for flext-web.

Provides TestsFlextWebProtocols, combining p with
FlextWebProtocols for test-specific protocol definitions.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from flext_tests import p

from flext_web import FlextWebProtocols


class TestsFlextWebProtocols(p, FlextWebProtocols):
    """Test protocols combining p and FlextWebProtocols.

    Provides access to:
    - p.Tests.Docker.* (from p)
    - p.Tests.Factory.* (from p)
    - p.Web.* (from FlextWebProtocols)
    """

    class Web(FlextWebProtocols.Web):
        """Web-specific test protocols."""

        class Tests:
            """Project-specific test protocols.

            Extends Tests Web-specific protocols.
            """


p = TestsFlextWebProtocols
__all__ = ["TestsFlextWebProtocols", "p"]
