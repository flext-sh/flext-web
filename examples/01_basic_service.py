"""Basic flext-web startup via the canonical public facade."""

from __future__ import annotations

from flext_web import web


def main() -> None:
    """Start flext-web using validated namespaced settings and the facade."""
    # Settings are validated at construction; overrides go through clone().
    settings = web.settings.clone(
        Web={
            "host": "127.0.0.1",
            "port": 8000,
            "secret_key": "dev-secret-key-32-characters-long",
        },
        debug=True,
    )
    try:
        _ = web.start_service(
            host=settings.Web.host, port=settings.Web.port, debug=settings.debug
        )
    except KeyboardInterrupt:
        return
    except (RuntimeError, OSError, ValueError):
        raise


if __name__ == "__main__":
    main()
