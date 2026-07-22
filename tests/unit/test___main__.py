"""Unit tests for flext_web.__main__."""

from __future__ import annotations

from flext_tests import tm
from flext_web import __main__, web


class TestsFlextWebMain:
    """Tests for the CLI entry point."""

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

    def test_run_command_class_exposed(self) -> None:
        """The Pydantic-driven run command must be exported."""
        tm.that(__main__.FlextWebRunCommand, none=False)

    def test_main_callable_exposed(self) -> None:
        """The console entry point ``main`` must be callable."""
        tm.that(callable(__main__.main), eq=True)

    def test_main_help_returns_zero(self) -> None:
        """The CLI ``--help`` must exit with status zero through the facade."""
        return_code = __main__.main(["--help"])
        tm.that(return_code, eq=0)

    def test_run_command_help_returns_zero(self) -> None:
        """The ``run --help`` subcommand must exit with status zero."""
        return_code = __main__.main(["run", "--help"])
        tm.that(return_code, eq=0)

    def test_run_command_execute(self) -> None:
        """The run command model executes and delegates to the web facade."""
        cmd = __main__.FlextWebRunCommand(host="127.0.0.1", port=0, no_debug=True)
        result = cmd.execute()
        tm.fail(result)
        tm.that(result.error, none=False)
