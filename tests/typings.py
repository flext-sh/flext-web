"""Test type aliases for flext-web.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from flext_tests import FlextTestsTypes

from flext_web import FlextWebTypes


class FlextWebTestTypes(FlextTestsTypes, FlextWebTypes):
    """Test type aliases for flext-web."""

    class Web(FlextWebTypes.Web):
        """Web domain test type aliases."""

        class Tests:
            """Test-specific type aliases."""


t = FlextWebTestTypes
__all__ = ["FlextWebTestTypes", "t"]
