"""Test utilities for flext-web.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from flext_tests import FlextTestsUtilities

from flext_web import FlextWebUtilities


class FlextWebTestUtilities(FlextTestsUtilities, FlextWebUtilities):
    """Test utilities for flext-web."""

    class Web(FlextWebUtilities.Web):
        """Web domain test utilities."""

        class Tests:
            """Test-specific utilities."""


u = FlextWebTestUtilities
__all__ = ["FlextWebTestUtilities", "u"]
