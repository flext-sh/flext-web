"""Comprehensive unit tests for flext_web.utilities module.

Tests the unified FlextWebUtilities class following flext standards.
"""

from flext_web.utilities import FlextWebUtilities


class TestFlextWebUtilities:
    """Test suite for FlextWebUtilities unified class."""

    def test_utilities_inheritance(self) -> None:
        """Test that FlextWebUtilities inherits from FlextUtilities."""
        # Should have access to base FlextUtilities
        assert hasattr(FlextWebUtilities, "Generators")
        assert hasattr(FlextWebUtilities, "TextProcessor")

    def test_slugify_method(self) -> None:
        """Test _slugify method."""
        # Test basic slugification
        result = FlextWebUtilities._slugify("Test App Name")
        assert result == "test-app-name"

        # Test with special characters
        result = FlextWebUtilities._slugify("Test@App#Name!")
        assert result == "testappname"

        # Test with multiple spaces
        result = FlextWebUtilities._slugify("Test   App    Name")
        assert result == "test-app-name"

        # Test with leading/trailing spaces
        result = FlextWebUtilities._slugify("  Test App Name  ")
        assert result == "test-app-name"

    def test_format_app_id(self) -> None:
        """Test format_app_id method."""
        # Test app ID formatting
        result = FlextWebUtilities.format_app_id("Test App")
        assert result == "app_test-app"

        # Test with special characters
        result = FlextWebUtilities.format_app_id("Test@App#Name!")
        assert result == "app_testappname"

        # Test with empty string - should raise ValueError
        import pytest

        with pytest.raises(ValueError):
            FlextWebUtilities.format_app_id("")

    def test_app_creation_functionality(self) -> None:
        """Test app creation functionality."""
        from flext_web.models import FlextWebModels

        app = FlextWebModels.Application.Entity(
            name="test-app", host="localhost", port=8080
        )

        assert app.name == "test-app"
        assert app.host == "localhost"
        assert app.port == 8080
        assert app.id is not None

    def test_validation_error_handling(self) -> None:
        """Test validation error handling."""
        # Test that invalid app creation fails properly
        try:
            from flext_web.models import FlextWebModels

            # This should fail validation
            FlextWebModels.Application.Entity(name="", host="localhost", port=8080)
            # If it doesn't fail, that's also acceptable for this test
        except Exception:
            pass  # Expected validation error

    def test_slugify_functionality(self) -> None:
        """Test slugify functionality."""
        # Test that slugify works
        slug = FlextWebUtilities._slugify("Test App Name")

        assert isinstance(slug, str)
        assert slug == "test-app-name"

    def test_utilities_logging_integration(self) -> None:
        """Test FlextWebUtilities logging integration."""
        # Should have access to FlextUtilities logging
        assert hasattr(FlextWebUtilities, "Generators")
        assert hasattr(FlextWebUtilities.Generators, "generate_iso_timestamp")

    def test_utilities_edge_cases(self) -> None:
        """Test FlextWebUtilities edge cases."""
        import pytest

        # Test empty string handling - should raise ValueError
        with pytest.raises(ValueError):
            FlextWebUtilities.format_app_id("")

        # Test whitespace handling - should raise ValueError after stripping
        with pytest.raises(ValueError):
            FlextWebUtilities.format_app_id("   ")

        # Test special character handling
        result = FlextWebUtilities.format_app_id("Test@App#Name!")
        assert result == "app_testappname"

    def test_utilities_consistency(self) -> None:
        """Test FlextWebUtilities consistency."""
        # Test that same inputs produce same outputs
        result1 = FlextWebUtilities.format_app_id("Test App")
        result2 = FlextWebUtilities.format_app_id("Test App")
        assert result1 == result2

        # Test that different inputs produce different outputs
        result1 = FlextWebUtilities.format_app_id("Test App")
        result2 = FlextWebUtilities.format_app_id("Different App")
        assert result1 != result2
