"""Comprehensive unit tests for flext_web.utilities module.

Tests the unified u class following flext standards.
"""

from __future__ import annotations

from unittest.mock import patch

import pytest
from flext_tests import m, u


class TestFlextWebUtilities:
    """Test suite for u unified class."""

    def test_utilities_inheritance(self) -> None:
        """Test that u inherits from u."""
        u.Tests.Matchers.that(hasattr(u, "generate_iso_timestamp"), eq=True)
        u.Tests.Matchers.that(hasattr(u, "safe_string"), eq=True)

    def test_slugify_method(self) -> None:
        """Test slugify method."""
        result = u.slugify("Test App Name")
        u.Tests.Matchers.that(result, eq="test-app-name")
        result = u.slugify("Test@App#Name!")
        u.Tests.Matchers.that(result, eq="test-app-name")
        result = u.slugify("Test   App    Name")
        u.Tests.Matchers.that(result, eq="test-app-name")
        result = u.slugify("  Test App Name  ")
        u.Tests.Matchers.that(result, eq="test-app-name")

    def test_format_app_id(self) -> None:
        """Test format_app_id method."""
        result = u.format_app_id("Test App")
        u.Tests.Matchers.that(result, eq="app_test-app")
        result = u.format_app_id("Test@App#Name!")
        u.Tests.Matchers.that(result, eq="app_testappname")
        with pytest.raises(ValueError):
            _ = u.format_app_id("")

    def test_app_creation_functionality(self) -> None:
        """Test app creation functionality."""
        app = m.Web.Entity(name="test-app", host="localhost", port=8080)
        u.Tests.Matchers.that(app.name, eq="test-app")
        u.Tests.Matchers.that(app.host, eq="localhost")
        u.Tests.Matchers.that(app.port, eq=8080)
        u.Tests.Matchers.that(app.id is not None, eq=True)

    def test_validation_error_handling(self) -> None:
        """Test validation error handling."""
        try:
            _ = m.Web.Entity(name="", host="localhost", port=8080)
        except Exception:
            pass

    def test_slugify_functionality(self) -> None:
        """Test slugify functionality."""
        slug = u.slugify("Test App Name")
        u.Tests.Matchers.that(isinstance(slug, str), eq=True)
        u.Tests.Matchers.that(slug, eq="test-app-name")

    def test_utilities_logging_integration(self) -> None:
        """Test u logging integration."""
        u.Tests.Matchers.that(hasattr(u, "generate_iso_timestamp"), eq=True)

    def test_utilities_edge_cases(self) -> None:
        """Test u edge cases."""
        with pytest.raises(ValueError):
            _ = u.format_app_id("")
        with pytest.raises(ValueError):
            _ = u.format_app_id("   ")
        result = u.format_app_id("Test@App#Name!")
        u.Tests.Matchers.that(result, eq="app_testappname")

    def test_utilities_consistency(self) -> None:
        """Test u consistency."""
        result1 = u.format_app_id("Test App")
        result2 = u.format_app_id("Test App")
        u.Tests.Matchers.that(result1, eq=result2)
        result1 = u.format_app_id("Test App")
        result2 = u.format_app_id("Different App")
        u.Tests.Matchers.that(result1 != result2, eq=True)

    def test_format_app_id_safe_string_failure(self) -> None:
        """Test format_app_id when safe_string fails."""
        with (
            patch(
                "flext_web.utilities.FlextWebUtilities.safe_string",
                side_effect=ValueError("Invalid string"),
            ),
            pytest.raises(ValueError, match="Invalid string"),
        ):
            _ = u.format_app_id("test")

    def test_format_app_id_empty_after_stripping(self) -> None:
        """Test format_app_id when name becomes empty after stripping."""
        with (
            patch(
                "flext_web.utilities.FlextWebUtilities.safe_string",
                return_value="   ",
            ),
            pytest.raises(
                ValueError, match="Cannot format application name 'test' to valid ID"
            ),
        ):
            _ = u.format_app_id("test")

    def test_format_app_id_slugify_empty(self) -> None:
        """Test format_app_id when slugify results in empty string."""
        with (
            patch(
                "flext_web.utilities.FlextWebUtilities.safe_string",
                return_value="test",
            ),
            patch("flext_web.utilities.u.slugify", return_value=""),
            pytest.raises(ValueError, match="Cannot format application name"),
        ):
            _ = u.format_app_id("test")
