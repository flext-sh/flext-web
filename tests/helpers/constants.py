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

        These type aliases reuse production Literals from FlextWebConstants
        to ensure consistency between tests and production code.
        """

        # Reuse production Literals for consistency (Python 3.13+ best practices)
        # HTTP method literal (reusing production type)
        HttpMethodLiteral: TypeAlias = FlextWebConstants.Literals.HttpMethodLiteral

        # Environment name literal (reusing production type)
        EnvironmentNameLiteral: TypeAlias = (
            FlextWebConstants.Literals.EnvironmentNameLiteral
        )

        # Application status literal (reusing production type)
        ApplicationStatusLiteral: TypeAlias = (
            FlextWebConstants.Literals.ApplicationStatusLiteral
        )

        # Application type literal (reusing production type)
        ApplicationTypeLiteral: TypeAlias = (
            FlextWebConstants.Literals.ApplicationTypeLiteral
        )

        # Response status literal (reusing production type)
        ResponseStatusLiteral: TypeAlias = (
            FlextWebConstants.Literals.ResponseStatusLiteral
        )

        # Protocol literal (reusing production type)
        ProtocolLiteral: TypeAlias = FlextWebConstants.Literals.ProtocolLiteral

        # Content type literal (reusing production type)
        ContentTypeLiteral: TypeAlias = FlextWebConstants.Literals.ContentTypeLiteral

        # Session cookie SameSite literal (reusing production type)
        SameSiteLiteral: TypeAlias = FlextWebConstants.Literals.SameSiteLiteral


# Standardized short name for use in tests (same pattern as flext-core)
c = TestsConstants

__all__ = ["TestsConstants", "c"]
