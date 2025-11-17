"""Unit tests for flext_web.__main__ module.

Tests the CLI entry point functionality following flext standards.
"""

from __future__ import annotations

from unittest.mock import Mock, patch

from flext_core import FlextResult

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

    def test_run_success(self) -> None:
        """Test run method with successful service status."""
        cli_service = __main__.FlextWebCliService()

        # Mock API to return success - use real ServiceResponse structure
        mock_status = FlextWebModels.Service.ServiceResponse(
            service="flext-web",
            status="healthy",
            capabilities=["http_services_available"],
            config=True,
        )
        with patch.object(
            cli_service._api,
            "get_service_status",
            return_value=FlextResult[FlextWebModels.Service.ServiceResponse].ok(
                mock_status
            ),
        ):
            result = cli_service.run()
            assert result.is_success
            assert result.unwrap() is True

    def test_run_failure(self) -> None:
        """Test run method with failed service status."""
        cli_service = __main__.FlextWebCliService()

        # Mock API to return failure
        with patch.object(
            cli_service._api,
            "get_service_status",
            return_value=FlextResult[FlextWebModels.Service.ServiceResponse].fail(
                "Service unavailable"
            ),
        ):
            result = cli_service.run()
            assert result.is_failure
            assert "Service unavailable" in result.error

    def test_log_status_and_return(self) -> None:
        """Test _log_status_and_return method."""
        cli_service = __main__.FlextWebCliService()

        # Use real ServiceResponse structure
        mock_status = FlextWebModels.Service.ServiceResponse(
            service="test-service",
            status="healthy",
            capabilities=["http_services_available"],
            config=True,
        )

        # Should return True and not raise exception
        result = cli_service._log_status_and_return(mock_status)
        assert result is True  # Should return True for successful status check


class TestMainFunction:
    """Test suite for main() function."""

    @patch("flext_web.__main__.sys.exit")
    def test_main_success(self, mock_exit: Mock) -> None:
        """Test main function with successful service."""
        # Use real ServiceResponse structure
        mock_status = FlextWebModels.Service.ServiceResponse(
            service="flext-web",
            status="healthy",
            capabilities=["http_services_available"],
            config=True,
        )

        with patch.object(
            __main__.FlextWebApi,
            "get_service_status",
            return_value=FlextResult[FlextWebModels.Service.ServiceResponse].ok(
                mock_status
            ),
        ):
            __main__.FlextWebCliService.main()
            # Should exit with code 0 on success
            mock_exit.assert_called_once_with(0)

    def test_main_failure(self) -> None:
        """Test main function with failed service."""
        from unittest.mock import call, patch

        with (
            patch.object(
                __main__.FlextWebApi,
                "get_service_status",
                return_value=FlextResult[FlextWebModels.Service.ServiceResponse].fail(
                    "Service error"
                ),
            ),
            patch("flext_web.__main__.sys.exit") as mock_exit,
        ):
            __main__.FlextWebCliService.main()
            # Should exit with code 1 on failure
            # sys.exit(1) should be called
            assert call(1) in mock_exit.call_args_list, (
                "sys.exit(1) should have been called"
            )

    def test_main_module_execution(self) -> None:
        """Test __main__ module execution (line 78)."""
        # Test that the module can be executed
        # This covers the if __name__ == "__main__" line
        import subprocess
        import sys

        # Execute the module directly
        result = subprocess.run(
            [sys.executable, "-m", "flext_web.__main__"],
            check=False,
            capture_output=True,
            text=True,
            timeout=5,
        )
        # Should exit (either 0 or 1 depending on service status)
        assert result.returncode in {0, 1}
