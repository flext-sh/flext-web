"""Test utility definitions for flext-web.

Provides TestsFlextWebUtilities, extending u and FlextWebUtilities
for test-specific utility functions. Pattern established for future test helpers.

Inheritance hierarchy:
- u (flext_tests) - Provides .Tests.* namespace
- FlextWebUtilities (production) - Provides .Web.* namespace

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from flext_tests import u

from flext_web import FlextWebUtilities


class TestsFlextWebUtilities(FlextWebUtilities, u):
    """Test utilities combining u and FlextWebUtilities.

    Access: u.Tests.* (from u), u.Web.* (from FlextWebUtilities)
    Add test-specific utilities under u.Web.Tests when needed.
    """

    class Web(FlextWebUtilities.Web):
        """Web namespace extending FlextWebUtilities.Web."""

        class Tests:
            """Test-specific web utilities (add helpers when needed)."""


u = TestsFlextWebUtilities
__all__ = ["TestsFlextWebUtilities", "u"]
