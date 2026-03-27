"""Unit tests for flext_web.__main__."""

from __future__ import annotations

import pytest
from flext_tests import tm

from flext_web import FlextWebProtocols, __main__, web


class TestFlextWebCliService:
    """Tests for the CLI adapter."""

    def setup_method(self) -> None:
        """Reset shared runtime registries before each test."""
        FlextWebProtocols.Web.apps_registry.clear()
        FlextWebProtocols.Web.framework_instances.clear()
        FlextWebProtocols.Web.app_runtimes.clear()
        FlextWebProtocols.Web.web_metrics.clear()
        FlextWebProtocols.Web.service_state.update({
            "routes_initialized": False,
            "middleware_configured": False,
            "service_running": False,
        })

    def test_initialization(self) -> None:
        """The CLI defaults to the canonical `web` facade."""
        cli_service = __main__.FlextWebCliService()
        tm.that(cli_service._api is web, eq=True)

    def test_parse_args(self) -> None:
        """The parser accepts host, port and debug flags."""
        args = __main__.FlextWebCliService.parse_args([
            "--host",
            "127.0.0.1",
            "--port",
            "8195",
            "--debug",
        ])
        tm.that(args.host, eq="127.0.0.1")
        tm.that(args.port, eq=8195)
        tm.that(args.debug, eq=True)

    def test_run_starts_service(self) -> None:
        """Running the CLI starts the service through the public facade."""
        cli_service = __main__.FlextWebCliService()
        result = cli_service.run(["--host", "127.0.0.1", "--port", "8196"])
        tm.ok(result)
        tm.that(FlextWebProtocols.Web.service_state["service_running"], eq=True)
        stop_result = web.stop_service()
        tm.ok(stop_result)


class TestMainFunction:
    """Tests for the console entrypoint."""

    def test_main_structure(self) -> None:
        """The module exposes the console callable required by pyproject."""
        tm.that(callable(__main__.main), eq=True)
        tm.that(callable(__main__.FlextWebCliService.main), eq=True)

    def test_main_module_execution(self) -> None:
        """The console entrypoint exits with code zero on success."""
        with pytest.raises(SystemExit) as exc_info:
            __main__.FlextWebCliService.main([
                "--host",
                "127.0.0.1",
                "--port",
                "8197",
            ])
        tm.that(exc_info.value.code, eq=0)
        stop_result = web.stop_service()
        tm.ok(stop_result)
