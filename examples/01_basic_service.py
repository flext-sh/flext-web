"""Basic flext-web startup via the canonical public facade."""

from __future__ import annotations

import os

from flext_web import web


class FlextWebExamples:
    """FlextWeb example facade for the basic service startup."""

    def main(self) -> None:
        """Start flext-web using validated namespaced settings and the facade."""
        # Settings are validated at construction; overrides go through clone().
        settings = web.settings.clone(
            Web={
                "host": "127.0.0.1",
                "port": 8000,
                "secret_key": os.environ.get("FLEXT_WEB_SECRET_KEY", "<demo-secret>"),
            },
            debug=True,
        )
        _ = web.start_service(
            host=settings.Web.host, port=settings.Web.port, debug=settings.debug
        )


examples_flext_web = FlextWebExamples()


if __name__ == "__main__":
    examples_flext_web.main()
