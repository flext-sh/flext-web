"""Unit tests for flext_web.__main__ module.

Tests the CLI entry point functionality following flext standards.
"""

from __future__ import annotations

import pytest
from flext_web import __main__
from flext_web.models import FlextWebModels


class TestFlextWebCliService:
    """Test suite for FlextWebCliService class."""

    def test_initialization(self) -> None:
        """Test FlextWebCliService initialization."""
        cli_service = __main__.FlextWebCliService()
        assert cli_service is not None
        assert hasattr(cli_service, "_logger")
        assert hasattr(cli_service, "_api")

    def test_log_status_and_return(self) -> None:
        """Test _log_status_and_return method."""
        cli_service = __main__.FlextWebCliService()

        # Use real ServiceResponse structure
        status = FlextWebModels.Web.ServiceResponse(
            service="test-service",
            status="healthy",
            capabilities=["http_services_available"],
            config=True,
        )

        # Should return True and not raise exception
        result = cli_service._log_status_and_return(status)
        assert result is True  # Should return True for successful status check


class TestMainFunction:
    """Test suite for main() function."""

    def test_main_structure(self) -> None:
        """Test main function structure and imports."""
        # Test that main function exists and is callable
        assert callable(__main__.FlextWebCliService.main)
        assert hasattr(__main__.FlextWebCliService, "main")

    def test_main_module_execution(self) -> None:
        """Test __main__ module execution (line 78)."""
        # Test that the module can be executed
        # This covers the if __name__ == "__main__" line
        # Execute the main function directly

        with pytest.raises(SystemExit) as exc_info:
            __main__.FlextWebCliService.main()
        assert exc_info.value.code == 0
