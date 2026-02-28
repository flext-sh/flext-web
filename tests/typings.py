"""Test typing definitions for flext-web.

Provides TestsFlextWebTypes, extending FlextTestsTypes and FlextWebTypes
for test-specific type aliases and factory functions. Pattern established.

Inheritance hierarchy:
- FlextTestsTypes (flext_tests) - Provides .Tests.* namespace
- FlextWebTypes (production) - Provides .Web.* namespace

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from flext_tests import FlextTestsTypes
from flext_web import FlextWebTypes


class TestsFlextWebTypes(FlextTestsTypes, FlextWebTypes):
    """Test typings combining FlextTestsTypes and FlextWebTypes.

    Access: t.Tests.* (from FlextTestsTypes), t.Web.* (from FlextWebTypes)
    Add test-specific type aliases under t.Web.Tests when needed.
    """

    class Web(FlextWebTypes.Web):
        """Web namespace extending FlextWebTypes.Web."""

        class Tests:
            """Test-specific web typings (add aliases when needed)."""


# Runtime alias per FLEXT convention
t = TestsFlextWebTypes

__all__ = ["TestsFlextWebTypes", "t"]
