"""Console entry point for flext-web."""

from __future__ import annotations

import argparse
import sys

from flext_core import r
from flext_web import FlextWeb, FlextWebSettings, t, web


class FlextWebCliService:
    """CLI adapter over the canonical `web` facade."""

    def __init__(self, api: FlextWeb | None = None) -> None:
        """Initialize the CLI with a facade instance."""
        super().__init__()
        self._api = api if api is not None else web

    @staticmethod
    def build_parser() -> argparse.ArgumentParser:
        """Build the CLI argument parser."""
        parser = argparse.ArgumentParser(prog="flext-web")
        parser.add_argument("--host", default=None)
        parser.add_argument("--port", type=int, default=None)
        parser.add_argument("--debug", action="store_true")
        parser.add_argument("--no-debug", action="store_true")
        return parser

    @classmethod
    def parse_args(
        cls,
        argv: t.StrSequence | None = None,
    ) -> argparse.Namespace:
        """Parse CLI arguments."""
        return cls.build_parser().parse_args(list(argv) if argv is not None else None)

    @classmethod
    def main(cls, argv: t.StrSequence | None = None) -> None:
        """CLI entry point following the console script contract."""
        result = cls().run(argv)
        sys.exit(0 if result.is_success else 1)

    def run(self, argv: t.StrSequence | None = None) -> r[bool]:
        """Run the public web facade from CLI arguments."""
        args = self.parse_args(argv)
        debug_value = False if args.no_debug else bool(args.debug)
        config_result = FlextWebSettings.create_web_config(
            host=args.host,
            port=args.port,
            debug=debug_value,
        )
        if config_result.is_failure:
            return r[bool].fail(config_result.error)
        service_result = self._api.create_service(config_result.value)
        if service_result.is_failure:
            return r[bool].fail(service_result.error)
        return service_result.value.start_service(
            host=config_result.value.host,
            port=config_result.value.port,
            debug=debug_value,
        )


def main() -> None:
    """Console script shim required by pyproject entry points."""
    FlextWebCliService.main(sys.argv[1:])


if __name__ == "__main__":
    main()

__all__ = ["FlextWebCliService", "main"]
