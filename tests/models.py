"""Test model definitions for flext-web.

Provides TestsFlextWebModels, extending m and FlextWebModels
for test-specific model definitions. Pattern established for future test fixtures.

Inheritance hierarchy:
- m (flext_tests) - Provides .Tests.* namespace
- FlextWebModels (production) - Provides .Web.* namespace

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from flext_tests import m

from flext_web import FlextWebModels


class TestsFlextWebModels(m):
    """Test models combining m and FlextWebModels.Web.

    Access: m.Tests.* (from m), m.Web.* (from FlextWebModels.Web)
    Add test-specific models under m.Web.Tests when needed.
    """

    class Web(FlextWebModels.Web):
        """Web namespace extending FlextWebModels.Web."""

        class Tests:
            """Test-specific web models (add fixtures, factories when needed)."""


# Runtime alias per FLEXT convention
m = TestsFlextWebModels

__all__ = ["TestsFlextWebModels", "m"]
