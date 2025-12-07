"""Test constants for flext-web tests.

Centralized constants for test fixtures, factories, and test data.
Does NOT duplicate src/flext_web/constants.py - only test-specific constants.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from typing import Final, TypeAlias

from flext_web.constants import FlextWebConstants


class TestsConstants(FlextWebConstants):
    """Centralized test constants following flext-core nested class pattern."""

    class Paths:
        """Test path constants."""

        TEST_INPUT_DIR: Final[str] = "tests/fixtures/data/input"
        TEST_OUTPUT_DIR: Final[str] = "tests/fixtures/data/output"
        TEST_TEMP_PREFIX: Final[str] = "flext_web_test_"

    class Web:
        """Web test server constants."""

        DEFAULT_HOST: Final[str] = "localhost"
        DEFAULT_PORT: Final[int] = 8080
        TEST_APP_NAME: Final[str] = "TestApplication"
        CONNECTION_TIMEOUT: Final[float] = 5.0
        OPERATION_TIMEOUT: Final[float] = 10.0

    class Http:
        """HTTP test constants."""

        TEST_ENDPOINT: Final[str] = "/test"
        TEST_METHOD: Final[str] = "GET"
        TEST_CONTENT_TYPE: Final[str] = "application/json"

    class Literals:
        """Literal type aliases for test constants (Python 3.13 pattern).

        These type aliases reuse production Literals from FlextWebConstants.Web
        to ensure consistency between tests and production code.
        All Literal types are now at FlextWebConstants.Web level for direct access.
        """

        # Reuse production Literals for consistency (Python 3.13+ best practices)
        # HTTP method literal (reusing production type from Web level)
        HttpMethodLiteral: TypeAlias = FlextWebConstants.Web.HttpMethodLiteral

        # Environment name literal (reusing production type from Web level)
        EnvironmentNameLiteral: TypeAlias = FlextWebConstants.Web.EnvironmentNameLiteral

        # Application status literal (reusing production type from Web level)
        ApplicationStatusLiteral: TypeAlias = (
            FlextWebConstants.Web.ApplicationStatusLiteral
        )

        # Application type literal (reusing production type from Web level)
        ApplicationTypeLiteral: TypeAlias = FlextWebConstants.Web.ApplicationTypeLiteral

        # Response status literal (reusing production type from Web level)
        ResponseStatusLiteral: TypeAlias = FlextWebConstants.Web.ResponseStatusLiteral

        # Protocol literal (reusing production type from Web level)
        ProtocolLiteral: TypeAlias = FlextWebConstants.Web.ProtocolLiteral

        # Content type literal (reusing production type from Web level)
        ContentTypeLiteral: TypeAlias = FlextWebConstants.Web.ContentTypeLiteral

        # Session cookie SameSite literal (reusing production type from Web level)
        SameSiteLiteral: TypeAlias = FlextWebConstants.Web.SameSiteLiteral


# Standardized short name for use in tests (same pattern as flext-core)
c = TestsConstants

__all__ = ["TestsConstants", "c"]
