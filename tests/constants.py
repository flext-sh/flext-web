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

        class Tests:
            """Test-specific constants."""

            class Paths:
                """Test path constants."""

                TEST_INPUT_DIR: Final[str] = "tests/fixtures/data/input"
                TEST_OUTPUT_DIR: Final[str] = "tests/fixtures/data/output"
                TEST_TEMP_PREFIX: Final[str] = "flext_web_test_"

            class TestWeb:
                """Web test server constants."""

                DEFAULT_HOST: Final[str] = "localhost"
                DEFAULT_PORT: Final[int] = 8080
                TEST_APP_NAME: Final[str] = "TestApplication"
                CONNECTION_TIMEOUT: Final[float] = 5.0
                OPERATION_TIMEOUT: Final[float] = 10.0

            class TestPort:
                """Port allocation constants for test isolation."""

                PORT_START: Final[int] = 9000
                PORT_END: Final[int] = 9999

            class TestHttp:
                """HTTP test constants."""

                TEST_ENDPOINT: Final[str] = "/test"
                TEST_METHOD: Final[str] = "GET"
                TEST_CONTENT_TYPE: Final[str] = "application/json"

            class Literals:
                """Literal type aliases for test constants (Python 3.13 pattern).

                These type aliases use the StrEnum types from FlextWebConstants.Web
                to ensure consistency between tests and production code.
                """

                type HttpMethodLiteral = FlextWebConstants.Web.Method
                type EnvironmentNameLiteral = FlextWebConstants.Web.Name
                type ApplicationStatusLiteral = FlextWebConstants.Web.Status
                type ApplicationTypeLiteral = FlextWebConstants.Web.ApplicationType
                type ResponseStatusLiteral = str
                type ProtocolLiteral = str
                type ContentTypeLiteral = str
                type SameSiteLiteral = str


c = TestsFlextWebConstants
__all__: list[str] = ["TestsFlextWebConstants", "c"]
