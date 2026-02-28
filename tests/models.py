"""Test model definitions for flext-web.

Provides TestsFlextWebModels, extending FlextTestsModels and FlextWebModels
for test-specific model definitions. Pattern established for future test fixtures.

Inheritance hierarchy:
- FlextTestsModels (flext_tests) - Provides .Tests.* namespace
- FlextWebModels (production) - Provides .Web.* namespace

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from flext_tests import FlextTestsModels
from flext_web import FlextWebModels


class TestsFlextWebModels(FlextTestsModels):
    """Test models combining FlextTestsModels and FlextWebModels.Web.

    Access: m.Tests.* (from FlextTestsModels), m.Web.* (from FlextWebModels.Web)
    Add test-specific models under m.Web.Tests when needed.
    """

    class Web(FlextWebModels.Web):
        """Web namespace extending FlextWebModels.Web."""

        class Tests:
            """Test-specific web models (add fixtures, factories when needed)."""


# Runtime alias per FLEXT convention
m = TestsFlextWebModels

__all__ = ["TestsFlextWebModels", "m"]
