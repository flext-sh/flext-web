"""Constants for flext-web tests.

Provides TestsFlextWebConstants, extending FlextTestsConstants with flext-web-specific
constants using COMPOSITION INHERITANCE.

Inheritance hierarchy:
- FlextTestsConstants (flext_tests) - Provides .Tests.* namespace
- FlextWebConstants (production) - Provides .Web.* namespace

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from typing import Final, TypeAlias

from flext_tests.constants import FlextTestsConstants

from flext_web.constants import FlextWebConstants


class TestsFlextWebConstants(FlextTestsConstants, FlextWebConstants):
    """Constants for flext-web tests using COMPOSITION INHERITANCE.

    MANDATORY: Inherits from BOTH:
    1. FlextTestsConstants - for test infrastructure (.Tests.*)
    2. FlextWebConstants - for domain constants (.Web.*)

    Access patterns:
    - tc.Tests.Docker.* (container testing)
    - tc.Tests.Matcher.* (assertion messages)
    - tc.Tests.Factory.* (test data generation)
    - tc.Web.* (domain constants from production)
    - tc.TestWeb.* (project-specific test data)

    Rules:
    - NEVER duplicate constants from FlextTestsConstants or FlextWebConstants
    - Only flext-web-specific test constants allowed (not generic for other projects)
    - All generic constants come from FlextTestsConstants
    - All production constants come from FlextWebConstants
    """

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

    class TestHttp:
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
        HttpMethodLiteral: TypeAlias = FlextWebConstants.Web.HttpMethodLiteral
        EnvironmentNameLiteral: TypeAlias = FlextWebConstants.Web.EnvironmentNameLiteral
        ApplicationStatusLiteral: TypeAlias = (
            FlextWebConstants.Web.ApplicationStatusLiteral
        )
        ApplicationTypeLiteral: TypeAlias = FlextWebConstants.Web.ApplicationTypeLiteral
        ResponseStatusLiteral: TypeAlias = FlextWebConstants.Web.ResponseStatusLiteral
        ProtocolLiteral: TypeAlias = FlextWebConstants.Web.ProtocolLiteral
        ContentTypeLiteral: TypeAlias = FlextWebConstants.Web.ContentTypeLiteral
        SameSiteLiteral: TypeAlias = FlextWebConstants.Web.SameSiteLiteral


# Short aliases per FLEXT convention
tc = TestsFlextWebConstants  # Primary test constants alias
c = TestsFlextWebConstants  # Alternative alias for compatibility

__all__ = [
    "TestsFlextWebConstants",
    "c",
    "tc",
]
