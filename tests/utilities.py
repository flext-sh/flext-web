"""Test utility definitions for flext-web.

Provides TestsFlextWebUtilities, extending FlextTestsUtilities and FlextWebUtilities
for test-specific utility functions. Pattern established for future test helpers.

Inheritance hierarchy:
- FlextTestsUtilities (flext_tests) - Provides .Tests.* namespace
- FlextWebUtilities (production) - Provides .Web.* namespace

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from flext_tests import FlextTestsUtilities
from flext_web import FlextWebUtilities


class TestsFlextWebUtilities(FlextTestsUtilities, FlextWebUtilities):
    """Test utilities combining FlextTestsUtilities and FlextWebUtilities.

    Access: u.Tests.* (from FlextTestsUtilities), u.Web.* (from FlextWebUtilities)
    Add test-specific utilities under u.Web.Tests when needed.
    """

    class Web(FlextWebUtilities.Web):
        """Web namespace extending FlextWebUtilities.Web."""

        class Tests:
            """Test-specific web utilities (add helpers when needed)."""


# Runtime alias per FLEXT convention
u = TestsFlextWebUtilities

__all__ = ["TestsFlextWebUtilities", "u"]
