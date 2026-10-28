"""Test type aliases for flext-web.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from flext_tests import FlextTestsTypes

from flext_web import FlextWebTypes


class TestsFlextWebTypes(FlextWebTypes, FlextTestsTypes):
    """Test type aliases for flext-web."""

    class Tests(FlextTestsTypes.Tests):
        """Web domain test type aliases."""


t = TestsFlextWebTypes
__all__: list[str] = ["TestsFlextWebTypes", "t"]
