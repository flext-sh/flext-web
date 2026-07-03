"""Test constants for flext-web.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from typing import Final

from flext_tests import FlextTestsConstants

from flext_web import FlextWebConstants


class TestsFlextWebConstants(FlextTestsConstants, FlextWebConstants):
    """Test constants for flext-web."""

    class Web(FlextWebConstants.Web):
        """Web domain test constants."""

        class Tests(FlextTestsConstants.Tests):
            """Test-specific constants."""

            DEFAULT_HOST: Final[str] = "localhost"
            DEFAULT_PORT: Final[int] = 8080
            TEST_APP_NAME: Final[str] = "TestApplication"
            PORT_START: Final[int] = 9000
            PORT_END: Final[int] = 9999
            TEST_METHOD: Final[str] = "GET"
            TEST_CONTENT_TYPE: Final[str] = "application/json"


c = TestsFlextWebConstants
__all__: list[str] = ["TestsFlextWebConstants", "c"]
