"""Test constants for flext-web.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from typing import ClassVar

from flext_tests import FlextTestsConstants

from flext_web import FlextWebConstants


class TestsFlextWebConstants(FlextWebConstants, FlextTestsConstants):
    """Test constants for flext-web."""

    class Tests(FlextTestsConstants.Tests):
        """Web domain test constants."""

        DEFAULT_HOST: ClassVar[str] = "localhost"
        DEFAULT_PORT: ClassVar[int] = 8080
        TEST_APP_NAME: ClassVar[str] = "TestApplication"
        PORT_START: ClassVar[int] = 9000
        PORT_END: ClassVar[int] = 9999
        TEST_METHOD: ClassVar[str] = "GET"
        TEST_CONTENT_TYPE: ClassVar[str] = "application/json"


c = TestsFlextWebConstants
__all__: list[str] = ["TestsFlextWebConstants", "c"]
