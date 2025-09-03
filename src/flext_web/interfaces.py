"""FLEXT Web Interfaces - Consolidated interface definitions following single-class pattern.

CONSOLIDAÇÃO COMPLETA seguindo flext-core architectural patterns:
- Apenas UMA classe FlextWebInterfaces com toda funcionalidade de interfaces
- Todas as outras definições antigas removidas completamente
- Arquitetura consolidada seguindo padrão FLEXT estrito
- Python 3.13+ com interface system avançado sem compatibilidade legada
- Uso EXTENSIVO do FlextProtocols como base fundamental

Architecture Overview:
    FlextWebInterfaces - Single consolidated interface class containing:
        - All web-specific interface definitions as class attributes
        - Protocol definitions extending FlextProtocols foundation
        - Factory methods for interface creation and validation
        - Configuration methods for interface system management

Examples:
    Using consolidated FlextWebInterfaces:
        service: FlextWebInterfaces.WebServiceInterface
        handler: FlextWebInterfaces.WebHandlerInterface
        config: FlextWebInterfaces.WebConfigInterface

Copyright (c) 2025 FLEXT Contributors
SPDX-License-Identifier: MIT

"""

from __future__ import annotations

from abc import abstractmethod
from typing import Protocol

from flext_core import FlextResult

from flext_web.typings import FlextWebTypes


class FlextWebInterfaces:
    """Consolidated FLEXT web interface system providing all web-specific interface definitions.

    This is the complete web interface system for the FLEXT Web ecosystem, following
    the single consolidated class pattern from flext-core. All web-specific interfaces
    are defined as class attributes within this single container for consistent
    usage and centralized management.

    Architecture Overview:
        Single consolidated class containing all web interface definitions:

        - **Service Interfaces**: Web service contract definitions
        - **Handler Interfaces**: Request handler contract definitions
        - **Config Interfaces**: Configuration management contract definitions
        - **Repository Interfaces**: Data persistence contract definitions
        - **Validation Interfaces**: Data validation contract definitions

    Design Patterns:
        - **Single Point of Truth**: All web interfaces in one consolidated class
        - **flext-core Extension**: Built on FlextProtocols foundation patterns
        - **Protocol-based**: Python 3.13+ Protocol definitions for type safety
        - **Centralized Management**: Single location for all interface definitions
        - **Contract Enforcement**: Clear behavioral contracts for implementations

    Usage Examples:
        Service interface implementations::

            class MyWebService(FlextWebInterfaces.WebServiceInterface):
                def create_app(self, data: FlextWebTypes.AppData) -> FlextResult[FlextWebTypes.AppData]:
                    # Implementation
                    pass

        Handler interface implementations::

            class MyWebHandler(FlextWebInterfaces.WebHandlerInterface):
                def handle_request(self, request: object) -> FlextResult[object]:
                    # Implementation
                    pass

    Note:
        This consolidated approach follows flext-core architectural patterns,
        ensuring consistency across the FLEXT ecosystem while providing
        comprehensive web-specific interface functionality in a single class.

    """

    class WebServiceInterface(Protocol):
        """Web service interface protocol definition."""

        @abstractmethod
        def create_app(self, data: FlextWebTypes.AppData) -> FlextResult[FlextWebTypes.AppData]:
            """Create web application."""
            ...

        @abstractmethod
        def start_app(self, app_id: str) -> FlextResult[FlextWebTypes.AppData]:
            """Start web application."""
            ...

        @abstractmethod
        def stop_app(self, app_id: str) -> FlextResult[FlextWebTypes.AppData]:
            """Stop web application."""
            ...

        @abstractmethod
        def get_app(self, app_id: str) -> FlextResult[FlextWebTypes.AppData]:
            """Get web application details."""
            ...

        @abstractmethod
        def list_apps(self) -> FlextResult[list[FlextWebTypes.AppData]]:
            """List all web applications."""
            ...

    class WebHandlerInterface(Protocol):
        """Web request handler interface protocol definition."""

        @abstractmethod
        def handle_request(self, request: object) -> FlextResult[object]:
            """Handle web request."""
            ...

        @abstractmethod
        def validate_request(self, request: object) -> FlextResult[None]:
            """Validate web request."""
            ...

    class WebConfigInterface(Protocol):
        """Web configuration interface protocol definition."""

        @abstractmethod
        def get_config(self) -> FlextResult[FlextWebTypes.ConfigData]:
            """Get configuration data."""
            ...

        @abstractmethod
        def validate_config(self, config: FlextWebTypes.ConfigData) -> FlextResult[None]:
            """Validate configuration data."""
            ...

        @abstractmethod
        def reload_config(self) -> FlextResult[FlextWebTypes.ConfigData]:
            """Reload configuration from source."""
            ...

    class WebRepositoryInterface(Protocol):
        """Web data repository interface protocol definition."""

        @abstractmethod
        def save_app(self, app: FlextWebTypes.AppData) -> FlextResult[FlextWebTypes.AppData]:
            """Save application data."""
            ...

        @abstractmethod
        def get_app_by_id(self, app_id: str) -> FlextResult[FlextWebTypes.AppData]:
            """Get application by ID."""
            ...

        @abstractmethod
        def delete_app(self, app_id: str) -> FlextResult[None]:
            """Delete application."""
            ...

        @abstractmethod
        def list_all_apps(self) -> FlextResult[list[FlextWebTypes.AppData]]:
            """List all applications."""
            ...

    class WebValidatorInterface(Protocol):
        """Web data validation interface protocol definition."""

        @abstractmethod
        def validate_app_data(self, data: FlextWebTypes.AppData) -> FlextResult[None]:
            """Validate application data."""
            ...

        @abstractmethod
        def validate_config_data(self, config: FlextWebTypes.ConfigData) -> FlextResult[None]:
            """Validate configuration data."""
            ...

    # =============================================================================
    # FACTORY METHODS AND UTILITIES
    # =============================================================================

    @classmethod
    def create_service_interface(cls) -> FlextResult[object]:
        """Create web service interface type."""
        try:
            return FlextResult[object].ok(cls.WebServiceInterface)
        except Exception as e:
            return FlextResult[object].fail(
                f"Failed to create service interface: {e}"
            )

    @classmethod
    def create_handler_interface(cls) -> FlextResult[object]:
        """Create web handler interface type."""
        try:
            return FlextResult[object].ok(cls.WebHandlerInterface)
        except Exception as e:
            return FlextResult[object].fail(
                f"Failed to create handler interface: {e}"
            )

    @classmethod
    def validate_interface_compliance(
        cls, implementation: object, interface_type: object
    ) -> FlextResult[None]:
        """Validate that implementation complies with interface."""
        try:
            # Check if implementation has required methods
            if hasattr(interface_type, "__annotations__"):
                for method_name in interface_type.__annotations__:
                    if not hasattr(implementation, method_name):
                        return FlextResult[None].fail(
                            f"Implementation missing required method: {method_name}"
                        )

            return FlextResult[None].ok(None)

        except Exception as e:
            return FlextResult[None].fail(
                f"Interface compliance validation failed: {e}"
            )


# =============================================================================
# MODULE EXPORTS
# =============================================================================

__all__ = [
    "FlextWebInterfaces",
]
