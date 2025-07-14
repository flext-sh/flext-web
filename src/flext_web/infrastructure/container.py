"""Dependency injection container for FLEXT-WEB."""

from __future__ import annotations

from flext_core.config import get_container, singleton
from flext_web.config import WebConfig


class WebContainerConfig:
    """Web container configuration using flext-core patterns."""

    def __init__(self, settings: WebConfig) -> None:
        self.settings = settings

    def configure_dependencies(self) -> None:
        """Configure dependency injection container with web-specific dependencies.

        Registers web configuration settings and container configuration instance
        in the flext-core dependency injection container.
        """
        container = get_container()

        # Register settings
        container.register(WebConfig, self.settings)

        # Register this config instance
        container.register(WebContainerConfig, self)


def setup_web_container(settings: WebConfig | None = None) -> WebContainerConfig:
    if settings is None:
        settings = WebConfig()

    config = WebContainerConfig(settings)
    config.configure_dependencies()

    return config


def get_web_container() -> WebContainerConfig:
    container = get_container()
    return container.resolve(WebContainerConfig)
