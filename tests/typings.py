"""Test typing definitions for flext-web.

Provides TestsFlextWebTypes, extending t and FlextWebTypes
for test-specific type aliases and factory functions. Pattern established.

Inheritance hierarchy:
- t (flext_tests) - Provides .Tests.* namespace
- FlextWebTypes (production) - Provides .Web.* namespace

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from flext_tests import t

from flext_web import FlextWebTypes


class TestsFlextWebTypes(t, FlextWebTypes):
    """Test typings combining t and FlextWebTypes.

    Access: t.Tests.* (from t), t.Web.* (from FlextWebTypes)
    Add test-specific type aliases under t.Web.Tests when needed.
    """

    class Web(FlextWebTypes.Web):
        """Web namespace extending FlextWebTypes.Web."""

        class Tests:
            """Test-specific web typings (add aliases when needed)."""


t = TestsFlextWebTypes
__all__ = ["TestsFlextWebTypes", "t"]
