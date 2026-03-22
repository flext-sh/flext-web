"""Unit tests for flext_web.__main__ module.

Tests the CLI entry point functionality following flext standards.
"""

from __future__ import annotations

import pytest
from flext_tests import m, tm

from flext_web import __main__


class TestFlextWebCliService:
    """Test suite for FlextWebCliService class."""

    def test_initialization(self) -> None:
        """Test FlextWebCliService initialization."""
        cli_service = __main__.FlextWebCliService()
        tm.that(cli_service is not None, eq=True)
        tm.that(hasattr(cli_service, "_logger"), eq=True)
        tm.that(hasattr(cli_service, "_api"), eq=True)

    def test_log_status_and_return(self) -> None:
        """Test _log_status_and_return method."""
        cli_service = __main__.FlextWebCliService()
        status = m.Web.ServiceResponse(
            service="test-service",
            status="healthy",
            capabilities=["http_services_available"],
            config=True,
        )
        result = cli_service._log_status_and_return(status)
        tm.that(result is True, eq=True)


class TestMainFunction:
    """Test suite for main() function."""

    def test_main_structure(self) -> None:
        """Test main function structure and imports."""
        tm.that(callable(__main__.FlextWebCliService.main), eq=True)
        tm.that(hasattr(__main__.FlextWebCliService, "main"), eq=True)

    def test_main_module_execution(self) -> None:
        """Test __main__ module execution (line 78)."""
        with pytest.raises(SystemExit) as exc_info:
            __main__.FlextWebCliService.main()
        tm.that(exc_info.value.code, eq=0)
