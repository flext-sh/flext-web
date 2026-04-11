"""Basic flext-web startup via the canonical public facade."""

from __future__ import annotations

from flext_web import web


def main() -> None:
    """Start flext-web using validated settings and the public facade."""
    config_result = web.settings.create_web_config(
        host="127.0.0.1",
        port=8000,
        debug=True,
        secret_key="dev-secret-key-32-characters-long",
    )
    if config_result.failure:
        return
    try:
        _ = web.start_service(
            host=config_result.value.host,
            port=config_result.value.port,
            debug=config_result.value.debug_mode,
        )
    except KeyboardInterrupt:
        return
    except (RuntimeError, OSError, ValueError):
        raise


if __name__ == "__main__":
    main()
