"""CLI facade for flext-web.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

import sys
from typing import Annotated, override

from flext_cli import cli, m as cli_m, p as cli_p, u as cli_u

from flext_web import FlextWebSettings, p, r, s, settings, t, web


class FlextWebCli:
    """CLI composition root for the flext-web service launcher."""

    class Run(s):
        """Pydantic-driven run command for the flext-web service."""

        host: Annotated[
            str | None,
            cli_u.Field(default=None, description="Bind host (overrides settings)."),
        ] = None
        port: Annotated[
            int | None,
            cli_u.Field(default=None, description="Bind port (overrides settings)."),
        ] = None
        debug: Annotated[
            bool, cli_u.Field(default=False, description="Enable debug mode.")
        ] = False
        no_debug: Annotated[
            bool, cli_u.Field(default=False, description="Force disable debug mode.")
        ] = False

        @override
        def execute(self) -> p.Result[bool]:
            """Apply CLI overrides and start the public web facade."""
            debug_value = False if self.no_debug else self.debug
            web_overrides: t.MutableMappingKV[str, str | int] = {}
            if self.host is not None:
                web_overrides["host"] = self.host
            if self.port is not None:
                web_overrides["port"] = self.port
            settings_result = r[FlextWebSettings].create_from_callable(
                lambda: settings.clone(Web=web_overrides, debug=debug_value)
            )
            if settings_result.failure:
                return r[bool].fail(settings_result.error)
            web_settings = settings_result.value
            service_result = web.create_service(web_settings)
            if service_result.failure:
                return r[bool].fail(service_result.error)
            return service_result.value.start_service(
                host=web_settings.Web.host,
                port=web_settings.Web.port,
                debug=debug_value,
            )

    @classmethod
    def build_app(cls) -> cli_p.Cli.Application:
        """Build the CLI application with the canonical result routes."""
        app = cli.create_app_with_common_params(
            name="flext-web", help_text="flext-web HTTP service launcher."
        )
        cli.register_result_routes(
            app,
            [
                cli_m.Cli.ResultCommandRoute(
                    name="run",
                    help_text="Start the flext-web service.",
                    model_cls=cls.Run,
                    handler=cls.execute_run_command,
                )
            ],
        )
        return app

    @staticmethod
    def execute_run_command(params: FlextWebCli.Run) -> p.Result[bool]:
        """Execute the typed run command for the CLI route."""
        return params.execute()


def main(argv: t.StrSequence | None = None) -> int:
    """Return the process exit code for the flext-web console entry point."""
    app = FlextWebCli.build_app()
    outcome = cli.execute_app(
        app,
        prog_name="flext-web",
        args=list(argv) if argv is not None else sys.argv[1:],
    )
    return cli.finalize_result(outcome)


__all__: list[str] = ["FlextWebCli", "main"]
