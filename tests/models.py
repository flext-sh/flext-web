"""Test models for flext-web.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from flext_tests import FlextTestsModels

from flext_web import FlextWebModels


class FlextWebTestModels(FlextTestsModels, FlextWebModels):
    """Test models for flext-web."""

    class Web(FlextWebModels.Web):
        """Web domain test models."""

        class Tests:
            """Test-specific models."""


m = FlextWebTestModels
__all__ = ["FlextWebTestModels", "m"]
