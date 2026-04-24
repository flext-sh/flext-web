"""Unit tests for flext_web.__main__."""

from __future__ import annotations

import pytest
from flext_tests import tm

from flext_web import __main__, web


class TestsFlextWebMain:
    """Tests for the CLI adapter."""

    def setup_method(self) -> None:
        """Reset shared runtime state through the public facade before each test."""
        apps_result = web.list_apps()
        if apps_result.success:
            for app in apps_result.value:
                if app.status == "running":
                    _ = web.stop_app(app.id)
        status_result = web.service_status()
        if status_result.success and status_result.value.status == "operational":
            _ = web.stop_service()

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
        status_result = web.service_status()
        tm.ok(status_result)
        tm.that(status_result.value.status, eq="operational")
        stop_result = web.stop_service()
        tm.ok(stop_result)

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
