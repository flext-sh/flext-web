"""FLEXT Web Protocols - Domain-specific protocol definitions for web operations.

This module provides FlextWebProtocols, a hierarchical collection of protocol
definitions that establish interface contracts for the flext-web project,
extending p with web-specific protocol definitions.

ARCHITECTURE:
 Layer 0: Web foundation protocols (used within flext-web)
 Layer 1: Web domain protocols (web services, web repositories)
 Layer 2: Web application protocols (web handlers, web commands)
 Layer 3: Web infrastructure protocols (web connections, web logging)

PROTOCOL INHERITANCE:
 Protocols use inheritance to reduce duplication and create logical hierarchies.
 Example: WebAppManagerProtocol extends FlextProtocols.Domain.Service[object]

USAGE IN WEB PROJECT:
 Web services extend FlextWebProtocols with web-specific protocols:

 >>> class WebAppService(FlextWebProtocols.Web.WebAppManagerProtocol):
... # Web-specific extensions
... pass

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from collections.abc import Callable
from typing import Protocol, runtime_checkable

from flext_core.protocols import FlextProtocols
from flext_core.result import r

from flext_web.constants import c
from flext_web.typings import t
from flext_web.utilities import u


class FlextWebProtocols(FlextProtocols):
    """Hierarchical protocol definitions for FLEXT web ecosystem.

    Extends p with web-specific protocol definitions for the
    flext-web project, establishing interface contracts and enabling type-safe,
    structural typing compliance across web components.

    Architecture Position: Domain Layer (Web domain extensions)
    - Extends p with web-specific protocol definitions
    - Used by all web components for type checking and structural typing validation
    - No imports from higher layers (Application, Infrastructure)

    Key Distinction: These are WEB PROTOCOL DEFINITIONS, not implementations.
    Actual implementations live in their respective web service layers.

    STRUCTURAL TYPING (DUCK TYPING) - CORE DESIGN PRINCIPLE

    All FlextWebProtocols are @runtime_checkable, which means:

    1. Method Signatures Matter: Classes satisfy protocols by implementing
    required methods with correct signatures, not by explicit inheritance

    2. isinstance() Works: isinstance(obj, FlextWebProtocols.Web.WebAppManagerProtocol)
    returns True if obj implements all required methods with correct signatures

    3. Duck Typing Philosophy: "If it walks like a web app manager and manages
    like a web app manager, it's a web app manager"

    4. Metaclass Conflicts Prevented: @runtime_checkable protocols don't use
    ProtocolMeta with service metaclasses, avoiding inheritance conflicts

    5. Type Safety: Full mypy/pyright type checking without inheritance

    Example of structural typing:
    class WebApplicationService:
        '''Satisfies FlextWebProtocols.Web.WebAppManagerProtocol through method implementation.'''
        def create_app(self, name: str, port: int, host: str) -> r:
            '''Required method - protocol compliance verified.'''
            pass

    service = WebApplicationService()
    # isinstance(service, FlextWebProtocols.Web.WebAppManagerProtocol) → True (duck typing!)

    PROTOCOL HIERARCHY (4 LAYERS)

    **Layer 0: Web Foundation Protocols** (Core web building blocks)
    - WebAppManagerProtocol - Web application lifecycle management
    - WebResponseFormatterProtocol - Response formatting for web APIs
    - WebFrameworkInterfaceProtocol - Web framework integration

    **Layer 1: Web Domain Protocols** (Web business logic interfaces)
    - WebServiceProtocol - Base web service interface
    - WebRepositoryProtocol - Web data access interface

    **Layer 2: Web Application Protocols** (Web use case patterns)
    - WebHandlerProtocol - Web command/query handler interface
    - WebCommandBusProtocol - Web command routing and execution

    **Layer 3: Web Infrastructure Protocols** (Web external integrations)
    - WebConnectionProtocol - Web external system connection
    - WebLoggerProtocol - Web logging interface

    CORE PRINCIPLES (4 FUNDAMENTAL RULES)

    **1. Web protocols extend p with web-specific interfaces**
    - No unnecessary protocols for other projects
    - Web-specific protocols live in flext-web project
    - Other web projects (flext-api, flext-auth) extend with their specific protocols

    **2. Web protocols live in their respective web projects**
    - flext-web has FlextWebProtocols for web operations
    - Each web project extends p with domain-specific extensions
    - Allows type-safe web-specific interface definitions

    **3. Protocol inheritance creates logical web hierarchies**
    - WebAppManagerProtocol extends FlextProtocols.Domain.Service[object]
    - WebRepositoryProtocol extends p.Repository
    - Reduces duplication, improves maintainability

    **4. All web protocols are @runtime_checkable for isinstance() validation**
    - isinstance(obj, FlextWebProtocols.Web.WebAppManagerProtocol) validates compliance
    - Used for runtime type checking and validation in web components
    - Enables duck typing without metaclass conflicts

    EXTENSION PATTERN - HOW WEB PROJECTS USE p

    Web projects extend FlextWebProtocols with domain-specific protocols:

    **Example 1: Web Application Project**
    class FlextWebProtocols(p):
        class Web:
            class WebAppManagerProtocol(FlextProtocols.Domain.Service[object], Protocol):
                '''Web application management service.'''
                def create_app(self, name: str, port: int, host: str) -> r:
                    '''Create web application.'''
                    ...

    **Example 2: Web API Project**
    class FlextApiProtocols(p):
        class Api:
            class ApiServiceProtocol(FlextProtocols.Domain.Service[object], Protocol):
                '''API service operations.'''
                def handle_request(self, request: dict) -> r:
                    '''Handle API request.'''
                    ...

    INTEGRATION POINTS WITH FLEXT WEB ARCHITECTURE

    r Integration:
    - All result-returning methods defined with r[T] return type
    - Enables railway pattern error handling throughout web ecosystem
    - Type-safe success/failure composition

    FlextService Integration:
    - Base web service implementation follows Service protocol
    - Methods: execute(), validate_business_rules(), get_service_info()
    - Type-safe web service lifecycle management

    FlextModels Integration:
    - Web models satisfy HasModelDump, HasModelFields, ModelProtocol
    - Pydantic v2 integration through model_dump, model_fields, validate
    - Type-safe web domain model implementation

    PRODUCTION-READY CHARACTERISTICS

    Type Safety: @runtime_checkable protocols work with mypy/pyright strict
    Extensibility: Web projects extend with domain-specific protocols
    Integration: All web implementations follow protocol definitions
    No Breaking Changes: Protocol additions backward compatible
    Documentation: Each protocol documents use cases and extensions
    Performance: isinstance() checks optimized for runtime use

    CORE PRINCIPLES:
        1. Web protocols extend p with web-specific interfaces
        2. Web protocols live in their respective web projects
        3. Protocol inheritance creates logical web hierarchies
        4. All web protocols are @runtime_checkable for isinstance() validation

    ARCHITECTURAL LAYERS:
        - Foundation: Core web building blocks (app management, response formatting)
        - Domain: Web business logic protocols (web services, repositories)
        - Application: Web use case patterns (handlers, command bus)
        - Infrastructure: Web external integrations (connections, logging)

    EXTENSION PATTERN:
        Web projects extend FlextWebProtocols:

        >>> class FlextApiProtocols(FlextWebProtocols):
        ...     class Api:
        ...         class ApiServiceProtocol(FlextWebProtocols.Web.WebServiceProtocol):
        ...             pass
    """

    # =========================================================================
    # WEB: Web Domain-Specific Protocols
    # =========================================================================

    class Web:
        """Web domain-specific protocols.

        All web-specific protocols are organized within this namespace
        for proper namespace separation and cross-project access.
        """

        # =========================================================================
        # WEB FOUNDATION LAYER - Core web protocols used within flext-web
        # =========================================================================

        @runtime_checkable
        class WebAppManagerProtocol(FlextProtocols.Domain.Service[object], Protocol):
            """Protocol for web application lifecycle management.

            Extends FlextProtocols.Domain.Service[object] with web-specific application management
            operations. Provides standardized interface for creating, starting, stopping,
            and managing web applications.

            Used in: handlers.py (FlextWebHandlers.ApplicationHandler)
            """

            @staticmethod
            def create_app(
                name: str,
                port: int,
                host: str,
            ) -> FlextProtocols.Result[t.WebCore.ResponseDict]:
                """Create a new web application.

                Args:
                    name: Application name identifier
                    port: Network port for the application
                    host: Network host address for binding

                Returns:
                    r containing application data or error details

                """
                # Protocol implementation placeholder - parameters are part of interface contract
                _ = name, port, host  # pragma: no cover
                return r.fail("create_app method not implemented")

            @staticmethod
            def start_app(
                app_id: str,
            ) -> FlextProtocols.Result[t.WebCore.ResponseDict]:
                """Start a web application.

                Args:
                app_id: Unique identifier of the application to start

                Returns:
                r containing start operation result or error details

                """
                # Protocol implementation placeholder - parameter is part of interface contract
                _ = app_id  # pragma: no cover
                return r.fail("start_app method not implemented")

            @staticmethod
            def stop_app(
                app_id: str,
            ) -> FlextProtocols.Result[t.WebCore.ResponseDict]:
                """Stop a running web application.

                Args:
                app_id: Unique identifier of the application to stop

                Returns:
                r containing stop operation result or error details

                """
                # Protocol implementation placeholder - parameter is part of interface contract
                _ = app_id  # pragma: no cover
                return r.fail("stop_app method not implemented")

            @staticmethod
            def list_apps() -> FlextProtocols.Result[list[t.WebCore.ResponseDict]]:
                """List all web applications.

                Returns:
                r containing list of application data or error details

                """
                # Protocol implementation placeholder
                return r.fail("list_apps method not implemented")

        @runtime_checkable
        class WebResponseFormatterProtocol(
            FlextProtocols.Domain.Service[object],
            Protocol,
        ):
            """Protocol for web response formatting.

            Extends FlextProtocols.Domain.Service[object] with web-specific response formatting
            operations. Provides standardized interface for formatting success and
            error responses for web APIs.

            Used in: response formatters and API handlers
            """

            @staticmethod
            def format_success(data: t.WebCore.ResponseDict) -> t.WebCore.ResponseDict:
                """Format successful response data.

                Args:
                data: Response data to format

                Returns:
                Formatted response dictionary

                """
                # Protocol implementation placeholder - use u to simplify
                response: t.WebCore.ResponseDict = {
                    "status": c.Web.WebResponse.STATUS_SUCCESS,
                }
                # Use u.filter to merge valid data fields
                valid_data = u.filter(
                    data,
                    lambda _k, v: isinstance(v, (str, int, bool, list, dict)),
                )
                response.update(valid_data)
                return response

            @staticmethod
            def format_error(error: Exception) -> t.WebCore.ResponseDict:
                """Format error response data.

                Args:
                error: Exception to format as error response

                Returns:
                Formatted error response dictionary

                """
                # Protocol implementation placeholder
                result: t.WebCore.ResponseDict = {
                    "status": c.Web.WebResponse.STATUS_ERROR,
                    "message": str(error),
                }
                return result

            @staticmethod
            def create_json_response(
                data: t.WebCore.ResponseDict,
            ) -> t.WebCore.ResponseDict:
                """Create a JSON response.

                Args:
                data: Response data to serialize as JSON

                Returns:
                JSON response representation

                """
                # Protocol implementation placeholder - use u to simplify
                response: t.WebCore.ResponseDict = {
                    c.Web.Http.HEADER_CONTENT_TYPE: c.Web.Http.CONTENT_TYPE_JSON,
                }
                # Use u.filter to merge valid data fields
                valid_data = u.filter(
                    data,
                    lambda _k, v: isinstance(v, (str, int, bool, list, dict)),
                )
                response.update(valid_data)
                return response

            @staticmethod
            def get_request_data(
                _request: t.WebCore.RequestDict,
            ) -> t.WebCore.RequestDict:
                """Extract data from web request.

                Args:
                _request: Web request data (unused in placeholder)

                Returns:
                Extracted request data dictionary

                """
                # Protocol implementation placeholder - RequestDict is TypeAlias for dict
                # This is a placeholder implementation for the protocol definition
                empty_result: t.WebCore.RequestDict = {}
                return empty_result

        @runtime_checkable
        class WebFrameworkInterfaceProtocol(
            FlextProtocols.Domain.Service[object],
            Protocol,
        ):
            """Protocol for web framework integration.

            Extends FlextProtocols.Domain.Service[object] with web framework integration operations.
            Provides standardized interface for creating JSON responses, extracting
            request data, and handling JSON requests.

            Used in: web framework adapters and integration layers
            """

            @staticmethod
            def create_json_response(
                data: t.WebCore.ResponseDict,
            ) -> t.WebCore.ResponseDict:
                """Create a JSON response.

                Args:
                data: Response data to serialize as JSON

                Returns:
                JSON response representation

                """
                # Protocol implementation placeholder - use u to simplify
                response: t.WebCore.ResponseDict = {
                    c.Web.Http.HEADER_CONTENT_TYPE: c.Web.Http.CONTENT_TYPE_JSON,
                }
                # Use u.filter to merge valid data fields
                valid_data = u.filter(
                    data,
                    lambda _k, v: isinstance(v, (str, int, bool, list, dict)),
                )
                response.update(valid_data)
                return response

            @staticmethod
            def get_request_data(
                _request: t.WebCore.RequestDict,
            ) -> t.WebCore.RequestDict:
                """Extract data from web request.

                Args:
                _request: Web request data (unused in placeholder)

                Returns:
                Extracted request data dictionary

                """
                # Protocol implementation placeholder - RequestDict is TypeAlias for dict
                # This is a placeholder implementation for the protocol definition
                empty_result: t.WebCore.RequestDict = {}
                return empty_result

            @staticmethod
            def is_json_request(_request: t.WebCore.RequestDict) -> bool:
                """Check if request contains JSON data.

                Args:
                _request: Web request to check (unused in placeholder)

                Returns:
                True if request is JSON, False otherwise

                """
                # Protocol implementation placeholder - RequestDict is a Protocol
                # This is a placeholder implementation for the protocol definition
                return False  # pragma: no cover

        # =========================================================================
        # WEB DOMAIN LAYER - Web service and repository protocols
        # =========================================================================

        @runtime_checkable
        class WebServiceProtocol(FlextProtocols.Domain.Service[object], Protocol):
            """Base web service protocol.

            Extends FlextProtocols.Domain.Service[object] with web-specific service operations.
            Provides the foundation for all web services in the FLEXT web ecosystem.

            Used in: web service implementations
            """

            @staticmethod
            def initialize_routes() -> FlextProtocols.Result[bool]:
                """Initialize web service routes.

                Returns:
                r[bool]: Success contains True if routes initialized, failure with error details

                """
                # Protocol implementation placeholder
                return r[bool].ok(True)  # pragma: no cover

            @staticmethod
            def configure_middleware() -> FlextProtocols.Result[bool]:
                """Configure web service middleware.

                Returns:
                r[bool]: Success contains True if middleware configured, failure with error details

                """
                # Protocol implementation placeholder
                return r[bool].ok(True)  # pragma: no cover

            @staticmethod
            def start_service() -> FlextProtocols.Result[bool]:
                """Start the web service.

                Returns:
                r[bool]: Success contains True if service started, failure with error details

                """
                # Protocol implementation placeholder
                return r[bool].ok(True)  # pragma: no cover

            @staticmethod
            def stop_service() -> FlextProtocols.Result[bool]:
                """Stop the web service.

                Returns:
                r[bool]: Success contains True if service stopped, failure with error details

                """
                # Protocol implementation placeholder
                return r[bool].ok(True)  # pragma: no cover

        @runtime_checkable
        class WebRepositoryProtocol(
            FlextProtocols.Repository[t.WebCore.ResponseDict],
            Protocol,
        ):
            """Base web repository protocol for data access.

            Extends p.Repository with web-specific data access operations.
            Provides the foundation for repository implementations in web applications.

            Used in: web data access layers
            """

            @staticmethod
            def find_by_criteria(
                criteria: t.WebCore.RequestDict,
            ) -> FlextProtocols.Result[list[t.WebCore.ResponseDict]]:
                """Find entities by criteria.

                Args:
                criteria: Search criteria dictionary

                Returns:
                r containing list of matching entities or error details

                """
                # Protocol implementation placeholder - parameter is part of interface contract
                _ = criteria
                return r[list[t.WebCore.ResponseDict]].ok([])

        # =========================================================================
        # WEB APPLICATION LAYER - Web handler and command patterns
        # =========================================================================

        @runtime_checkable
        class WebHandlerProtocol(FlextProtocols.Handler, Protocol):
            """Web handler protocol for request/response patterns.

            Extends p.Handler with web-specific handler operations.
            Provides standardized interface for web request handling.

            Used in: web request handlers and controllers
            """

            def execute(
                self,
                command: t.FlexibleValue,
            ) -> FlextProtocols.Result[t.WebCore.ResponseDict]:
                """Execute command (extends p.Handler pattern).

                Args:
                    command: Command to execute

                Returns:
                    r containing response data or error details

                """
                ...

            @staticmethod
            def handle_request(
                request: t.WebCore.RequestDict,
            ) -> FlextProtocols.Result[t.WebCore.ResponseDict]:
                """Handle web request and return response.

                Args:
                request: Web request data

                Returns:
                r containing response data or error details

                """
                # Protocol implementation placeholder - parameter is part of interface contract
                _ = request
                return r[t.WebCore.ResponseDict].ok({})

        # =========================================================================
        # WEB INFRASTRUCTURE LAYER - Web external integrations
        # =========================================================================

        @runtime_checkable
        class WebConnectionProtocol(FlextProtocols.Domain.Service[object], Protocol):
            """Web connection protocol for external systems.

            Extends FlextProtocols.Domain.Service[object] with web-specific connection operations.
            Provides standardized interface for web service connections.

            Used in: web service adapters and external integrations
            """

            @staticmethod
            def get_endpoint_url() -> str:
                """Get the web service endpoint URL.

                Returns:
                Web service endpoint URL string

                """
                # Protocol implementation placeholder
                return "http://localhost:8080"  # pragma: no cover

        @runtime_checkable
        class WebLoggerProtocol(FlextProtocols.Domain.Service[object], Protocol):
            """Web logging protocol.

            Extends FlextProtocols.Domain.Service[object] with web-specific logging operations.
            Provides standardized interface for web application logging.

            Used in: web logging implementations
            """

            def log_request(
                self,
                request: t.WebCore.RequestDict,
                context: t.WebCore.RequestDict | None = None,
            ) -> None:
                """Log web request with context.

                Args:
                request: Web request data to log
                context: Additional logging context

                """

            def log_response(
                self,
                response: t.WebCore.ResponseDict,
                context: t.WebCore.ResponseDict | None = None,
            ) -> None:
                """Log web response with context.

                Args:
                response: Web response data to log
                context: Additional logging context

                """

        # =========================================================================
        # WEB TEMPLATE LAYER - Template rendering protocols
        # =========================================================================

        @runtime_checkable
        class WebTemplateRendererProtocol(
            FlextProtocols.Domain.Service[object],
            Protocol,
        ):
            """Protocol for web template rendering.

            Extends FlextProtocols.Domain.Service[object] with web template rendering operations.
            Provides standardized interface for template engine integration.

            Used in: web template rendering implementations
            """

            @staticmethod
            def render_template(
                template_name: str,
                context: t.WebCore.RequestDict,
            ) -> FlextProtocols.Result[str]:
                """Render template with context data.

                Args:
                template_name: Name of the template to render
                context: Template context data

                Returns:
                r containing rendered template string or error details

                """
                # Protocol implementation placeholder - parameters are part of interface contract
                _ = template_name, context
                return r[str].ok("")

            @staticmethod
            def render_dashboard(
                data: t.WebCore.ResponseDict,
            ) -> FlextProtocols.Result[str]:
                """Render dashboard template with data.

                Args:
                data: Dashboard data to render

                Returns:
                r containing rendered dashboard HTML or error details

                """
                # Protocol implementation placeholder - parameter is part of interface contract
                _ = data
                return r[str].ok("<html>Dashboard</html>")

        @runtime_checkable
        class WebTemplateEngineProtocol(
            FlextProtocols.Domain.Service[object],
            Protocol,
        ):
            """Protocol for web template engine operations.

            Extends FlextProtocols.Domain.Service[object] with template engine management operations.
            Provides interface for loading, validating, and managing templates.

            Used in: web template engine implementations
            """

            @staticmethod
            def load_template_config(
                config: t.WebCore.RequestDict,
            ) -> FlextProtocols.Result[bool]:
                """Load template engine configuration.

                Args:
                config: Template engine configuration

                Returns:
                r[bool]: Success contains True if config loaded, failure with error details

                """
                # Protocol implementation placeholder - parameter is part of interface contract
                _ = config
                return r[bool].ok(True)  # pragma: no cover

            @staticmethod
            def get_template_config() -> FlextProtocols.Result[t.WebCore.ResponseDict]:
                """Get current template engine configuration.

                Returns:
                r containing configuration data or error details

                """
                # Protocol implementation placeholder
                return r[t.WebCore.ResponseDict].ok({})

            @staticmethod
            def validate_template_config(
                config: t.WebCore.RequestDict,
            ) -> FlextProtocols.Result[bool]:
                """Validate template engine configuration.

                Args:
                config: Configuration to validate

                Returns:
                r[bool]: Success contains True if valid, failure with error details

                """
                # Protocol implementation placeholder - parameter is part of interface contract
                _ = config
                return r[bool].ok(True)  # pragma: no cover

            @staticmethod
            def render(
                template: str, context: t.WebCore.RequestDict
            ) -> FlextProtocols.Result[str]:
                """Render template string with context.

                Args:
                template: Template string to render
                context: Template context data

                Returns:
                r containing rendered template or error details

                """
                # Protocol implementation placeholder - parameters are part of interface contract
                _ = template, context
                return r[str].ok("")

            def add_filter(self, name: str, filter_func: Callable[[str], str]) -> None:
                """Add template filter function.

                Args:
                name: Filter name identifier
                filter_func: Filter function implementation

                """

            def add_global(
                self,
                name: str,
                *,
                value: str | int | bool | list[str] | dict[str, str | int | bool],
            ) -> None:
                """Add template global variable.

                Args:
                name: Global variable name
                value: Global variable value

                """

        # =========================================================================
        # WEB MONITORING LAYER - Observability and monitoring protocols
        # =========================================================================

        @runtime_checkable
        class WebMonitoringProtocol(FlextProtocols.Domain.Service[object], Protocol):
            """Web monitoring protocol for observability.

            Extends FlextProtocols.Domain.Service[object] with web-specific monitoring operations.
            Provides interface for web application metrics and health monitoring.

            Used in: web monitoring and observability implementations
            """

            def record_web_request(
                self,
                request: t.WebCore.RequestDict,
                response_time: float,
            ) -> None:
                """Record web request metrics.

                Args:
                request: Web request data
                response_time: Request response time in seconds

                """

            @staticmethod
            def get_web_health_status() -> t.WebCore.ResponseDict:
                """Get web application health status.

                Returns:
                Health status information dictionary

                """
                # Protocol implementation placeholder
                return {
                    "status": c.Web.WebResponse.STATUS_HEALTHY,
                    "service": c.Web.WebService.SERVICE_NAME,
                }

            @staticmethod
            def get_web_metrics() -> t.WebCore.ResponseDict:
                """Get web application metrics.

                Returns:
                Web metrics data dictionary

                """
                # Protocol implementation placeholder
                return {"requests": 0, "errors": 0, "uptime": "0s"}

        @runtime_checkable
        class ConfigValueProtocol(Protocol):
            """Protocol for configuration values."""

            def __str__(self) -> str:
                """Convert to string."""
                ...

            def __int__(self) -> int:
                """Convert to integer."""
                ...

            def __bool__(self) -> bool:
                """Convert to boolean."""
                ...

        @runtime_checkable
        class ResponseDataProtocol(Protocol):
            """Protocol for response data structures."""

            def get(
                self,
                key: str,
                default: str | None = None,
            ) -> str | int | bool | list[str] | None:
                """Get value by key with optional default."""
                ...


# Base implementation classes for testing
class _WebAppManagerBase:
    """Base implementation of WebAppManagerProtocol for testing."""

    def create_app(
        self,
        name: str,
        port: int,
        host: str,
    ) -> FlextProtocols.Result[t.WebCore.ResponseDict]:
        """Create a new web application."""
        return FlextWebProtocols.Web.WebAppManagerProtocol.create_app(name, port, host)

    def start_app(self, app_id: str) -> FlextProtocols.Result[t.WebCore.ResponseDict]:
        """Start a web application."""
        return FlextWebProtocols.Web.WebAppManagerProtocol.start_app(app_id)

    def stop_app(self, app_id: str) -> FlextProtocols.Result[t.WebCore.ResponseDict]:
        """Stop a running web application."""
        return FlextWebProtocols.Web.WebAppManagerProtocol.stop_app(app_id)

    def list_apps(
        self,
    ) -> FlextProtocols.Result[list[t.WebCore.ResponseDict]]:
        """List all web applications."""
        return FlextWebProtocols.Web.WebAppManagerProtocol.list_apps()


class _WebResponseFormatterBase:
    """Base implementation of WebResponseFormatterProtocol for testing."""

    def format_success(self, data: t.WebCore.ResponseDict) -> t.WebCore.ResponseDict:
        """Format successful response data."""
        return FlextWebProtocols.WebResponseFormatterProtocol.format_success(data)

    def format_error(self, error: Exception) -> t.WebCore.ResponseDict:
        """Format error response data."""
        return FlextWebProtocols.WebResponseFormatterProtocol.format_error(error)

    def create_json_response(
        self, data: t.WebCore.ResponseDict
    ) -> t.WebCore.ResponseDict:
        """Create a JSON response."""
        return FlextWebProtocols.WebResponseFormatterProtocol.create_json_response(data)

    def get_request_data(
        self, _request: t.WebCore.RequestDict
    ) -> t.WebCore.RequestDict:
        """Extract data from web request."""
        return FlextWebProtocols.WebResponseFormatterProtocol.get_request_data(_request)


class _WebFrameworkInterfaceBase:
    """Base implementation of WebFrameworkInterfaceProtocol for testing."""

    def create_json_response(
        self, data: t.WebCore.ResponseDict
    ) -> t.WebCore.ResponseDict:
        """Create a JSON response."""
        return FlextWebProtocols.WebFrameworkInterfaceProtocol.create_json_response(
            data,
        )

    def get_request_data(
        self, _request: t.WebCore.RequestDict
    ) -> t.WebCore.RequestDict:
        """Extract data from web request."""
        return FlextWebProtocols.WebFrameworkInterfaceProtocol.get_request_data(
            _request,
        )

    def is_json_request(self, _request: t.WebCore.RequestDict) -> bool:
        """Check if request contains JSON data."""
        return FlextWebProtocols.WebFrameworkInterfaceProtocol.is_json_request(_request)


class _WebServiceBase:
    """Base implementation of WebServiceProtocol for testing."""

    def initialize_routes(self) -> FlextProtocols.Result[bool]:
        """Initialize web service routes."""
        return FlextWebProtocols.Web.WebServiceProtocol.initialize_routes()

    def configure_middleware(self) -> FlextProtocols.Result[bool]:
        """Configure web service middleware."""
        return FlextWebProtocols.Web.WebServiceProtocol.configure_middleware()

    def start_service(self) -> FlextProtocols.Result[bool]:
        """Start the web service."""
        return FlextWebProtocols.Web.WebServiceProtocol.start_service()

    def stop_service(self) -> FlextProtocols.Result[bool]:
        """Stop the web service."""
        return FlextWebProtocols.Web.WebServiceProtocol.stop_service()


class _WebRepositoryBase:
    """Base implementation of WebRepositoryProtocol for testing."""

    def find_by_criteria(
        self,
        criteria: t.WebCore.RequestDict,
    ) -> FlextProtocols.Result[list[t.WebCore.ResponseDict]]:
        """Find entities by criteria."""
        return FlextWebProtocols.WebRepositoryProtocol.find_by_criteria(criteria)


class _WebHandlerBase:
    """Base implementation of WebHandlerProtocol for testing."""

    def handle_request(
        self,
        request: t.WebCore.RequestDict,
    ) -> FlextProtocols.Result[t.WebCore.ResponseDict]:
        """Handle web request and return response."""
        return FlextWebProtocols.Web.WebHandlerProtocol.handle_request(request)


class _WebConnectionBase:
    """Base implementation of WebConnectionProtocol for testing."""

    def get_endpoint_url(self) -> str:
        """Get the web service endpoint URL."""
        return FlextWebProtocols.WebConnectionProtocol.get_endpoint_url()


class _WebTemplateRendererBase:
    """Base implementation of WebTemplateRendererProtocol for testing."""

    def render_template(
        self,
        template_name: str,
        context: t.WebCore.RequestDict,
    ) -> FlextProtocols.Result[str]:
        """Render template with context data."""
        return FlextWebProtocols.WebTemplateRendererProtocol.render_template(
            template_name,
            context,
        )

    def render_dashboard(
        self, data: t.WebCore.ResponseDict
    ) -> FlextProtocols.Result[str]:
        """Render dashboard template with data."""
        return FlextWebProtocols.WebTemplateRendererProtocol.render_dashboard(data)


class _WebTemplateEngineBase:
    """Base implementation of WebTemplateEngineProtocol for testing."""

    def load_template_config(
        self, config: t.WebCore.RequestDict
    ) -> FlextProtocols.Result[bool]:
        """Load template engine configuration."""
        return FlextWebProtocols.WebTemplateEngineProtocol.load_template_config(config)

    def get_template_config(
        self,
    ) -> FlextProtocols.Result[t.WebCore.ResponseDict]:
        """Get current template engine configuration."""
        return FlextWebProtocols.WebTemplateEngineProtocol.get_template_config()

    def validate_template_config(
        self, config: t.WebCore.RequestDict
    ) -> FlextProtocols.Result[bool]:
        """Validate template engine configuration."""
        return FlextWebProtocols.WebTemplateEngineProtocol.validate_template_config(
            config,
        )

    def render(
        self, template: str, context: t.WebCore.RequestDict
    ) -> FlextProtocols.Result[str]:
        """Render template string with context."""
        return FlextWebProtocols.WebTemplateEngineProtocol.render(template, context)

    def add_filter(self, name: str, filter_func: Callable[[str], str]) -> None:
        """Add template filter function."""
        # Protocol implementation placeholder - parameters are part of interface contract
        _ = name, filter_func

    def add_global(
        self,
        name: str,
        *,
        value: str | int | bool | list[str] | dict[str, str | int | bool],
    ) -> None:
        """Add template global variable."""
        # Protocol implementation placeholder - parameters are part of interface contract
        _ = name, value


class _WebMonitoringBase:
    """Base implementation of WebMonitoringProtocol for testing."""

    def get_web_health_status(self) -> t.WebCore.ResponseDict:
        """Get web application health status."""
        return FlextWebProtocols.Web.WebMonitoringProtocol.get_web_health_status()

    def record_web_request(
        self,
        request: t.WebCore.RequestDict,
        response_time: float,
    ) -> None:
        """Record web request metrics."""
        # Protocol implementation placeholder
        _ = request, response_time

    def get_web_metrics(self) -> t.WebCore.ResponseDict:
        """Get web application metrics."""
        return FlextWebProtocols.Web.WebMonitoringProtocol.get_web_metrics()


# Runtime alias for simplified usage
p = FlextWebProtocols

__all__ = [
    "FlextWebProtocols",
    "_WebAppManagerBase",
    "_WebConnectionBase",
    "_WebFrameworkInterfaceBase",
    "_WebHandlerBase",
    "_WebMonitoringBase",
    "_WebRepositoryBase",
    "_WebServiceBase",
    "_WebTemplateEngineBase",
    "_WebTemplateRendererBase",
    "p",
]
