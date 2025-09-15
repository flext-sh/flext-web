"""Quick coverage test for remaining models.py lines.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

import pytest
from pydantic import ValidationError

from flext_web import FlextWebModels


class TestModelsQuickCoverage:
    """Quick tests to cover remaining models.py lines."""

    def test_status_validation_error_path(self) -> None:
        """Test status validation error path (lines 67-70)."""
        # Test invalid status during model creation
        with pytest.raises(ValidationError):
            FlextWebModels.WebApp(
                id="test_status_error",
                name="test-app",
                host="localhost",
                port=8080,
                status="invalid_status"
            )  # This will trigger the validation error

    def test_name_validation_reserved_words(self) -> None:
        """Test name validation with reserved words (lines 78-79, 83-84)."""
        # Test reserved words
        with pytest.raises(ValidationError, match="reserved"):
            FlextWebModels.WebApp(
                id="test_reserved",
                name="REDACTED_LDAP_BIND_PASSWORD",  # Reserved word
                host="localhost",
                port=8080,
            )

        # Test dangerous characters
        with pytest.raises(ValidationError, match="dangerous"):
            FlextWebModels.WebApp(
                id="test_dangerous",
                name="test<script>",  # Dangerous characters
                host="localhost",
                port=8080,
            )

    def test_host_validation_errors(self) -> None:
        """Test host validation error paths (lines 99-100, 105-106, 110-111)."""
        # Test empty host after sanitization
        with pytest.raises(ValidationError):
            FlextWebModels.WebApp(
                id="test_empty_host",
                name="test-app",
                host="",  # Empty host
                port=8080,
            )


__all__ = [
    "TestModelsQuickCoverage",
]
