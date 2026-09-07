"""Unit tests for flext_web.__main__."""

from __future__ import annotations

from flext_tests import tm
from flext_web import __main__


class TestsFlextWebMain:
    """Tests for the CLI entry point."""

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
