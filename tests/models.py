"""Test models for flext-web.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from flext_tests import FlextTestsModels

from flext_web import m


class TestsFlextWebModels(m, FlextTestsModels):
    """Test models for flext-web."""

    class Tests(FlextTestsModels.Tests):
        """Web domain test models."""


m = TestsFlextWebModels
__all__: list[str] = ["TestsFlextWebModels", "m"]
