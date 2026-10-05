"""Test protocols for flext-web.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from flext_tests import FlextTestsProtocols

from flext_web import FlextWebProtocols


class TestsFlextWebProtocols(FlextWebProtocols, FlextTestsProtocols):
    """Test protocols for flext-web."""

    class Tests(FlextTestsProtocols.Tests):
        """Web domain test protocols."""


p = TestsFlextWebProtocols
__all__: list[str] = ["TestsFlextWebProtocols", "p"]
