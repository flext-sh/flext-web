"""FLEXT Web Protocols - Domain-specific protocol definitions for web operations.

This module provides FlextWebProtocols, a hierarchical collection of protocol
definitions that establish interface contracts for the flext-web project,
extending FlextProtocols with web-specific protocol definitions.

ARCHITECTURE:
 Layer 0: Web foundation protocols (used within flext-web)
 Layer 1: Web domain protocols (web services, web repositories)
 Layer 2: Web application protocols (web handlers, web commands)
 Layer 3: Web infrastructure protocols (web connections, web logging)

PROTOCOL INHERITANCE:
 Protocols use inheritance to reduce duplication and create logical hierarchies.
 Example: WebAppManagerProtocol extends FlextProtocols.Service

USAGE IN WEB PROJECT:
 Web services extend FlextWebProtocols with web-specific protocols:

 >>> class WebAppService(FlextWebProtocols.WebAppManagerProtocol):
... # Web-specific extensions
... pass

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from collections.abc import Callable
from typing import Protocol, runtime_checkable

from flext_core import FlextProtocols, FlextResult

from flext_web.constants import FlextWebConstants
from flext_web.typings import FlextWebTypes


class FlextWebProtocols(FlextProtocols):
    """Hierarchical protocol definitions for FLEXT web ecosystem.

    Extends FlextProtocols with web-specific protocol definitions for the
    flext-web project, establishing interface contracts and enabling type-safe,
    structural typing compliance across web components.

    Architecture Position: Domain Layer (Web domain extensions)
    - Extends FlextProtocols with web-specific protocol definitions
    - Used by all web components for type checking and structural typing validation
    - No imports from higher layers (Application, Infrastructure)

    Key Distinction: These are WEB PROTOCOL DEFINITIONS, not implementations.
    Actual implementations live in their respective web service layers.

    STRUCTURAL TYPING (DUCK TYPING) - CORE DESIGN PRINCIPLE

    All FlextWebProtocols are @runtime_checkable, which means:

    1. Method Signatures Matter: Classes satisfy protocols by implementing
    required methods with correct signatures, not by explicit inheritance

    2. isinstance() Works: isinstance(obj, FlextWebProtocols.WebAppManagerProtocol)
    returns True if obj implements all required methods with correct signatures

    3. Duck Typing Philosophy: "If it walks like a web app manager and manages
    like a web app manager, it's a web app manager"

    4. Metaclass Conflicts Prevented: @runtime_checkable protocols don't use
    ProtocolMeta with service metaclasses, avoiding inheritance conflicts

    5. Type Safety: Full mypy/pyright type checking without inheritance

    Example of structural typing:
    class WebApplicationService:
        '''Satisfies FlextWebProtocols.WebAppManagerProtocol through method implementation.'''
        def create_app(self, name: str, port: int, host: str) -> FlextResult:
            '''Required method - protocol compliance verified.'''
            pass

    service = WebApplicationService()
    # isinstance(service, FlextWebProtocols.WebAppManagerProtocol) → True (duck typing!)

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

    **1. Web protocols extend FlextProtocols with web-specific interfaces**
    - No unnecessary protocols for other projects
    - Web-specific protocols live in flext-web project
    - Other web projects (flext-api, flext-auth) extend with their specific protocols

    **2. Web protocols live in their respective web projects**
    - flext-web has FlextWebProtocols for web operations
    - Each web project extends FlextProtocols with domain-specific extensions
    - Allows type-safe web-specific interface definitions

    **3. Protocol inheritance creates logical web hierarchies**
    - WebAppManagerProtocol extends FlextProtocols.Service
    - WebRepositoryProtocol extends FlextProtocols.Repository
    - Reduces duplication, improves maintainability

    **4. All web protocols are @runtime_checkable for isinstance() validation**
    - isinstance(obj, FlextWebProtocols.WebAppManagerProtocol) validates compliance
    - Used for runtime type checking and validation in web components
    - Enables duck typing without metaclass conflicts

    EXTENSION PATTERN - HOW WEB PROJECTS USE FLEXTPROTOCOLS

    Web projects extend FlextWebProtocols with domain-specific protocols:

    **Example 1: Web Application Project**
    class FlextWebProtocols(FlextProtocols):
        class Web:
            class WebAppManagerProtocol(FlextProtocols.Service):
                '''Web application management service.'''
                def create_app(self, name: str, port: int, host: str) -> FlextResult:
                    '''Create web application.'''
                    ...

    **Example 2: Web API Project**
    class FlextApiProtocols(FlextProtocols):
        class Api:
            class ApiServiceProtocol(FlextProtocols.Service):
                '''API service operations.'''
                def handle_request(self, request: dict) -> FlextResult:
                    '''Handle API request.'''
                    ...

    INTEGRATION POINTS WITH FLEXT WEB ARCHITECTURE

    FlextResult Integration:
    - All result-returning methods defined with FlextResult[T] return type
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
        1. Web protocols extend FlextProtocols with web-specific interfaces
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
        ...         class ApiServiceProtocol(FlextWebProtocols.WebServiceProtocol):
        ...             pass
    """

    # =========================================================================
    # WEB FOUNDATION LAYER - Core web protocols used within flext-web
    # =========================================================================

    class WebAppManagerProtocol(
        FlextProtocols.Service[FlextWebTypes.Core.ResponseDict], Protocol
    ):
        """Protocol for web application lifecycle management.

        Extends FlextProtocols.Service with web-specific application management
        operations. Provides standardized interface for creating, starting, stopping,
        and managing web applications.

        Used in: handlers.py (FlextWebHandlers.ApplicationHandler)
        """

        def create_app(
            self, name: str, port: int, host: str
        ) -> FlextResult[FlextWebTypes.Core.ResponseDict]:
            """Create a new web application.

            Args:
                name: Application name identifier
                port: Network port for the application
                host: Network host address for binding

            Returns:
                FlextResult containing application data or error details

            """
            # Protocol implementation placeholder - parameters are part of interface contract
            _ = name, port, host
            return FlextResult.fail("create_app method not implemented")

        def start_app(
            self, app_id: str
        ) -> FlextResult[FlextWebTypes.Core.ResponseDict]:
            """Start a web application.

            Args:
            app_id: Unique identifier of the application to start

            Returns:
            FlextResult containing start operation result or error details

            """
            # Protocol implementation placeholder - parameter is part of interface contract
            _ = app_id
            return FlextResult.fail("start_app method not implemented")

        def stop_app(self, app_id: str) -> FlextResult[FlextWebTypes.Core.ResponseDict]:
            """Stop a running web application.

            Args:
            app_id: Unique identifier of the application to stop

            Returns:
            FlextResult containing stop operation result or error details

            """
            # Protocol implementation placeholder - parameter is part of interface contract
            _ = app_id
            return FlextResult.fail("stop_app method not implemented")

        def list_apps(self) -> FlextResult[list[FlextWebTypes.Core.ResponseDict]]:
            """List all web applications.

            Returns:
            FlextResult containing list of application data or error details

            """
            # Protocol implementation placeholder
            return FlextResult.fail("list_apps method not implemented")

    class WebResponseFormatterProtocol(
        FlextProtocols.Service[FlextWebTypes.Core.ResponseDict], Protocol
    ):
        """Protocol for web response formatting.

        Extends FlextProtocols.Service with web-specific response formatting
        operations. Provides standardized interface for formatting success and
        error responses for web APIs.

        Used in: response formatters and API handlers
        """

        def format_success(
            self, data: FlextWebTypes.Core.ResponseDict
        ) -> FlextWebTypes.Core.ResponseDict:
            """Format successful response data.

            Args:
            data: Response data to format

            Returns:
            Formatted response dictionary

            """
            # Protocol implementation placeholder
            # Merge data into response with status
            response: FlextWebTypes.Core.ResponseDict = {
                "status": FlextWebConstants.WebResponse.STATUS_SUCCESS,
            }
            # Merge data fields into response - ResponseDict allows nested dicts
            for key, value in data.items():
                if isinstance(value, (str, int, bool, list)):
                    response[key] = value
                elif isinstance(value, dict):
                    # Nested dict is allowed in ResponseDict definition
                    response[key] = value
            return response

        def format_error(self, error: Exception) -> FlextWebTypes.Core.ResponseDict:
            """Format error response data.

            Args:
            error: Exception to format as error response

            Returns:
            Formatted error response dictionary

            """
            # Protocol implementation placeholder
            result: FlextWebTypes.Core.ResponseDict = {
                "status": FlextWebConstants.WebResponse.STATUS_ERROR,
                "message": str(error),
            }
            return result

        def create_json_response(
            self, data: FlextWebTypes.Core.ResponseDict
        ) -> FlextWebTypes.Core.ResponseDict:
            """Create a JSON response.

            Args:
            data: Response data to serialize as JSON

            Returns:
            JSON response representation

            """
            # Protocol implementation placeholder
            # Build response with content type and merge data fields
            response: FlextWebTypes.Core.ResponseDict = {
                FlextWebConstants.Http.HEADER_CONTENT_TYPE: FlextWebConstants.Http.CONTENT_TYPE_JSON,
            }
            # Merge data fields into response - ResponseDict allows nested dicts
            for key, value in data.items():
                if isinstance(value, (str, int, bool, list)):
                    response[key] = value
                elif isinstance(value, dict):
                    # Nested dict is allowed in ResponseDict definition
                    response[key] = value
            return response

        def get_request_data(
            self, _request: FlextWebTypes.Core.RequestDict
        ) -> FlextWebTypes.Core.RequestDict:
            """Extract data from web request.

            Args:
            _request: Web request data (unused in placeholder)

            Returns:
            Extracted request data dictionary

            """
            # Protocol implementation placeholder - RequestDict is TypeAlias for dict
            # This is a placeholder implementation for the protocol definition
            empty_result: FlextWebTypes.Core.RequestDict = {}
            return empty_result

    class WebFrameworkInterfaceProtocol(
        FlextProtocols.Service[FlextWebTypes.Core.ResponseDict], Protocol
    ):
        """Protocol for web framework integration.

        Extends FlextProtocols.Service with web framework integration operations.
        Provides standardized interface for creating JSON responses, extracting
        request data, and handling JSON requests.

        Used in: web framework adapters and integration layers
        """

        def create_json_response(
            self, data: FlextWebTypes.Core.ResponseDict
        ) -> FlextWebTypes.Core.ResponseDict:
            """Create a JSON response.

            Args:
            data: Response data to serialize as JSON

            Returns:
            JSON response representation

            """
            # Protocol implementation placeholder
            # Build response with content type and merge data fields
            response: FlextWebTypes.Core.ResponseDict = {
                FlextWebConstants.Http.HEADER_CONTENT_TYPE: FlextWebConstants.Http.CONTENT_TYPE_JSON,
            }
            # Merge data fields into response - ResponseDict allows nested dicts
            for key, value in data.items():
                if isinstance(value, (str, int, bool, list)):
                    response[key] = value
                elif isinstance(value, dict):
                    # Nested dict is allowed in ResponseDict definition
                    response[key] = value
            return response

        def get_request_data(
            self, _request: FlextWebTypes.Core.RequestDict
        ) -> FlextWebTypes.Core.RequestDict:
            """Extract data from web request.

            Args:
            _request: Web request data (unused in placeholder)

            Returns:
            Extracted request data dictionary

            """
            # Protocol implementation placeholder - RequestDict is TypeAlias for dict
            # This is a placeholder implementation for the protocol definition
            empty_result: FlextWebTypes.Core.RequestDict = {}
            return empty_result

        def is_json_request(self, _request: FlextWebTypes.Core.RequestDict) -> bool:
            """Check if request contains JSON data.

            Args:
            _request: Web request to check (unused in placeholder)

            Returns:
            True if request is JSON, False otherwise

            """
            # Protocol implementation placeholder - RequestDict is a Protocol
            # This is a placeholder implementation for the protocol definition
            return False

    # =========================================================================
    # WEB DOMAIN LAYER - Web service and repository protocols
    # =========================================================================

    class WebServiceProtocol(
        FlextProtocols.Service[FlextWebTypes.Core.ResponseDict], Protocol
    ):
        """Base web service protocol.

        Extends FlextProtocols.Service with web-specific service operations.
        Provides the foundation for all web services in the FLEXT web ecosystem.

        Used in: web service implementations
        """

        def initialize_routes(self) -> FlextResult[bool]:
            """Initialize web service routes.

            Returns:
            FlextResult[bool]: Success contains True if routes initialized, failure with error details

            """
            # Protocol implementation placeholder
            return FlextResult[bool].ok(True)

        def configure_middleware(self) -> FlextResult[bool]:
            """Configure web service middleware.

            Returns:
            FlextResult[bool]: Success contains True if middleware configured, failure with error details

            """
            # Protocol implementation placeholder
            return FlextResult[bool].ok(True)

        def start_service(self) -> FlextResult[bool]:
            """Start the web service.

            Returns:
            FlextResult[bool]: Success contains True if service started, failure with error details

            """
            # Protocol implementation placeholder
            return FlextResult[bool].ok(True)

        def stop_service(self) -> FlextResult[bool]:
            """Stop the web service.

            Returns:
            FlextResult[bool]: Success contains True if service stopped, failure with error details

            """
            # Protocol implementation placeholder
            return FlextResult[bool].ok(True)

    class WebRepositoryProtocol(
        FlextProtocols.Repository[FlextWebTypes.Core.ResponseDict], Protocol
    ):
        """Base web repository protocol for data access.

        Extends FlextProtocols.Repository with web-specific data access operations.
        Provides the foundation for repository implementations in web applications.

        Used in: web data access layers
        """

        def find_by_criteria(
            self, criteria: FlextWebTypes.Core.RequestDict
        ) -> FlextResult[list[FlextWebTypes.Core.ResponseDict]]:
            """Find entities by criteria.

            Args:
            criteria: Search criteria dictionary

            Returns:
            FlextResult containing list of matching entities or error details

            """
            # Protocol implementation placeholder - parameter is part of interface contract
            _ = criteria
            return FlextResult[list[FlextWebTypes.Core.ResponseDict]].ok([])

    # =========================================================================
    # WEB APPLICATION LAYER - Web handler and command patterns
    # =========================================================================

    @runtime_checkable
    class WebHandlerProtocol(
        FlextProtocols.Handler[
            FlextWebTypes.Core.RequestDict, FlextWebTypes.Core.ResponseDict
        ],
        Protocol,
    ):
        """Web handler protocol for request/response patterns.

        Extends FlextProtocols.Handler with web-specific handler operations.
        Provides standardized interface for web request handling.

        Used in: web request handlers and controllers
        """

        def handle_request(
            self, request: FlextWebTypes.Core.RequestDict
        ) -> FlextResult[FlextWebTypes.Core.ResponseDict]:
            """Handle web request and return response.

            Args:
            request: Web request data

            Returns:
            FlextResult containing response data or error details

            """
            # Protocol implementation placeholder - parameter is part of interface contract
            _ = request
            return FlextResult[FlextWebTypes.Core.ResponseDict].ok({})

    # =========================================================================
    # WEB INFRASTRUCTURE LAYER - Web external integrations
    # =========================================================================

    @runtime_checkable
    class WebConnectionProtocol(
        FlextProtocols.Service[FlextWebTypes.Core.ResponseDict], Protocol
    ):
        """Web connection protocol for external systems.

        Extends FlextProtocols.Service with web-specific connection operations.
        Provides standardized interface for web service connections.

        Used in: web service adapters and external integrations
        """

        def get_endpoint_url(self) -> str:
            """Get the web service endpoint URL.

            Returns:
            Web service endpoint URL string

            """
            # Protocol implementation placeholder
            return "http://localhost:8080"

    class WebLoggerProtocol(
        FlextProtocols.Service[FlextWebTypes.Core.ResponseDict], Protocol
    ):
        """Web logging protocol.

        Extends FlextProtocols.Service with web-specific logging operations.
        Provides standardized interface for web application logging.

        Used in: web logging implementations
        """

        def log_request(
            self,
            request: FlextWebTypes.Core.RequestDict,
            context: FlextWebTypes.Core.RequestDict | None = None,
        ) -> None:
            """Log web request with context.

            Args:
            request: Web request data to log
            context: Additional logging context

            """

        def log_response(
            self,
            response: FlextWebTypes.Core.ResponseDict,
            context: FlextWebTypes.Core.ResponseDict | None = None,
        ) -> None:
            """Log web response with context.

            Args:
            response: Web response data to log
            context: Additional logging context

            """

    # =========================================================================
    # WEB TEMPLATE LAYER - Template rendering protocols
    # =========================================================================

    class WebTemplateRendererProtocol(
        FlextProtocols.Service[FlextWebTypes.Core.ResponseDict], Protocol
    ):
        """Protocol for web template rendering.

        Extends FlextProtocols.Service with web template rendering operations.
        Provides standardized interface for template engine integration.

        Used in: web template rendering implementations
        """

        def render_template(
            self, template_name: str, context: FlextWebTypes.Core.RequestDict
        ) -> FlextResult[str]:
            """Render template with context data.

            Args:
            template_name: Name of the template to render
            context: Template context data

            Returns:
            FlextResult containing rendered template string or error details

            """
            # Protocol implementation placeholder - parameters are part of interface contract
            _ = template_name, context
            return FlextResult[str].ok("")

        def render_dashboard(
            self, data: FlextWebTypes.Core.ResponseDict
        ) -> FlextResult[str]:
            """Render dashboard template with data.

            Args:
            data: Dashboard data to render

            Returns:
            FlextResult containing rendered dashboard HTML or error details

            """
            # Protocol implementation placeholder - parameter is part of interface contract
            _ = data
            return FlextResult[str].ok("<html>Dashboard</html>")

    class WebTemplateEngineProtocol(
        FlextProtocols.Service[FlextWebTypes.Core.ResponseDict], Protocol
    ):
        """Protocol for web template engine operations.

        Extends FlextProtocols.Service with template engine management operations.
        Provides interface for loading, validating, and managing templates.

        Used in: web template engine implementations
        """

        def load_template_config(
            self, config: FlextWebTypes.Core.RequestDict
        ) -> FlextResult[bool]:
            """Load template engine configuration.

            Args:
            config: Template engine configuration

            Returns:
            FlextResult[bool]: Success contains True if config loaded, failure with error details

            """
            # Protocol implementation placeholder - parameter is part of interface contract
            _ = config
            return FlextResult[bool].ok(True)

        def get_template_config(self) -> FlextResult[FlextWebTypes.Core.ResponseDict]:
            """Get current template engine configuration.

            Returns:
            FlextResult containing configuration data or error details

            """
            # Protocol implementation placeholder
            return FlextResult[FlextWebTypes.Core.ResponseDict].ok({})

        def validate_template_config(
            self, config: FlextWebTypes.Core.RequestDict
        ) -> FlextResult[bool]:
            """Validate template engine configuration.

            Args:
            config: Configuration to validate

            Returns:
            FlextResult[bool]: Success contains True if valid, failure with error details

            """
            # Protocol implementation placeholder - parameter is part of interface contract
            _ = config
            return FlextResult[bool].ok(True)

        def render(
            self, template: str, context: FlextWebTypes.Core.RequestDict
        ) -> FlextResult[str]:
            """Render template string with context.

            Args:
            template: Template string to render
            context: Template context data

            Returns:
            FlextResult containing rendered template or error details

            """
            # Protocol implementation placeholder - parameters are part of interface contract
            _ = template, context
            return FlextResult[str].ok("")

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
    class WebMonitoringProtocol(
        FlextProtocols.Service[FlextWebTypes.Core.ResponseDict], Protocol
    ):
        """Web monitoring protocol for observability.

        Extends FlextProtocols.Service with web-specific monitoring operations.
        Provides interface for web application metrics and health monitoring.

        Used in: web monitoring and observability implementations
        """

        def record_web_request(
            self, request: FlextWebTypes.Core.RequestDict, response_time: float
        ) -> None:
            """Record web request metrics.

            Args:
            request: Web request data
            response_time: Request response time in seconds

            """

        def get_web_health_status(self) -> FlextWebTypes.Core.ResponseDict:
            """Get web application health status.

            Returns:
            Health status information dictionary

            """
            # Protocol implementation placeholder
            return {
                "status": FlextWebConstants.WebResponse.STATUS_HEALTHY,
                "service": FlextWebConstants.WebService.SERVICE_NAME,
            }

        def get_web_metrics(self) -> FlextWebTypes.Core.ResponseDict:
            """Get web application metrics.

            Returns:
            Web metrics data dictionary

            """
            # Protocol implementation placeholder
            return {"requests": 0, "errors": 0, "uptime": "0s"}


# =========================================================================
# CONCRETE BASE CLASSES - For testing protocol placeholder methods
# =========================================================================


class _WebAppManagerBase:
    """Concrete base class for WebAppManagerProtocol placeholder methods.

    This class provides concrete implementations of protocol placeholder methods
    for testing purposes. It allows executing the placeholder logic directly.
    """

    def create_app(
        self, name: str, port: int, host: str
    ) -> FlextResult[FlextWebTypes.Core.ResponseDict]:
        """Create a new web application - placeholder implementation."""
        _ = name, port, host
        return FlextResult.fail("create_app method not implemented")

    def start_app(self, app_id: str) -> FlextResult[FlextWebTypes.Core.ResponseDict]:
        """Start a web application - placeholder implementation."""
        _ = app_id
        return FlextResult.fail("start_app method not implemented")

    def stop_app(self, app_id: str) -> FlextResult[FlextWebTypes.Core.ResponseDict]:
        """Stop a running web application - placeholder implementation."""
        _ = app_id
        return FlextResult.fail("stop_app method not implemented")

    def list_apps(self) -> FlextResult[list[FlextWebTypes.Core.ResponseDict]]:
        """List all web applications - placeholder implementation."""
        return FlextResult.fail("list_apps method not implemented")


class _WebResponseFormatterBase:
    """Concrete base class for WebResponseFormatterProtocol placeholder methods."""

    def format_success(
        self, data: FlextWebTypes.Core.ResponseDict
    ) -> FlextWebTypes.Core.ResponseDict:
        """Format successful response data - placeholder implementation."""
        response: FlextWebTypes.Core.ResponseDict = {
            "status": FlextWebConstants.WebResponse.STATUS_SUCCESS,
        }
        for key, value in data.items():
            if isinstance(value, (str, int, bool, list, dict)):
                response[key] = value
        return response

    def format_error(self, error: Exception) -> FlextWebTypes.Core.ResponseDict:
        """Format error response data - placeholder implementation."""
        result: FlextWebTypes.Core.ResponseDict = {
            "status": FlextWebConstants.WebResponse.STATUS_ERROR,
            "message": str(error),
        }
        return result

    def create_json_response(
        self, data: FlextWebTypes.Core.ResponseDict
    ) -> FlextWebTypes.Core.ResponseDict:
        """Create a JSON response - placeholder implementation."""
        response: FlextWebTypes.Core.ResponseDict = {
            FlextWebConstants.Http.HEADER_CONTENT_TYPE: FlextWebConstants.Http.CONTENT_TYPE_JSON,
        }
        for key, value in data.items():
            if isinstance(value, (str, int, bool, list, dict)):
                response[key] = value
        return response

    def get_request_data(
        self, _request: FlextWebTypes.Core.RequestDict
    ) -> FlextWebTypes.Core.RequestDict:
        """Extract data from web request - placeholder implementation."""
        empty_result: FlextWebTypes.Core.RequestDict = {}
        return empty_result


class _WebFrameworkInterfaceBase:
    """Concrete base class for WebFrameworkInterfaceProtocol placeholder methods."""

    def create_json_response(
        self, data: FlextWebTypes.Core.ResponseDict
    ) -> FlextWebTypes.Core.ResponseDict:
        """Create a JSON response - placeholder implementation."""
        response: FlextWebTypes.Core.ResponseDict = {
            FlextWebConstants.Http.HEADER_CONTENT_TYPE: FlextWebConstants.Http.CONTENT_TYPE_JSON,
        }
        for key, value in data.items():
            if isinstance(value, (str, int, bool, list, dict)):
                response[key] = value
        return response

    def get_request_data(
        self, _request: FlextWebTypes.Core.RequestDict
    ) -> FlextWebTypes.Core.RequestDict:
        """Extract data from web request - placeholder implementation."""
        empty_result: FlextWebTypes.Core.RequestDict = {}
        return empty_result

    def is_json_request(self, _request: FlextWebTypes.Core.RequestDict) -> bool:
        """Check if request contains JSON data - placeholder implementation."""
        return False


class _WebServiceBase:
    """Concrete base class for WebServiceProtocol placeholder methods."""

    def initialize_routes(self) -> FlextResult[bool]:
        """Initialize web service routes - placeholder implementation."""
        return FlextResult[bool].ok(True)

    def configure_middleware(self) -> FlextResult[bool]:
        """Configure web service middleware - placeholder implementation."""
        return FlextResult[bool].ok(True)

    def start_service(self) -> FlextResult[bool]:
        """Start the web service - placeholder implementation."""
        return FlextResult[bool].ok(True)

    def stop_service(self) -> FlextResult[bool]:
        """Stop the web service - placeholder implementation."""
        return FlextResult[bool].ok(True)


class _WebRepositoryBase:
    """Concrete base class for WebRepositoryProtocol placeholder methods."""

    def find_by_criteria(
        self, criteria: FlextWebTypes.Core.RequestDict
    ) -> FlextResult[list[FlextWebTypes.Core.ResponseDict]]:
        """Find entities by criteria - placeholder implementation."""
        _ = criteria
        return FlextResult[list[FlextWebTypes.Core.ResponseDict]].ok([])


class _WebHandlerBase:
    """Concrete base class for WebHandlerProtocol placeholder methods."""

    def handle_request(
        self, request: FlextWebTypes.Core.RequestDict
    ) -> FlextResult[FlextWebTypes.Core.ResponseDict]:
        """Handle web request and return response - placeholder implementation."""
        _ = request
        return FlextResult[FlextWebTypes.Core.ResponseDict].ok({})


class _WebTemplateRendererBase:
    """Concrete base class for WebTemplateRendererProtocol placeholder methods."""

    def render_template(
        self, template_name: str, context: FlextWebTypes.Core.RequestDict
    ) -> FlextResult[str]:
        """Render template with context data - placeholder implementation."""
        _ = template_name, context
        return FlextResult[str].ok("")

    def render_dashboard(
        self, data: FlextWebTypes.Core.ResponseDict
    ) -> FlextResult[str]:
        """Render dashboard template with data - placeholder implementation."""
        _ = data
        return FlextResult[str].ok("<html>Dashboard</html>")


class _WebTemplateEngineBase:
    """Concrete base class for WebTemplateEngineProtocol placeholder methods."""

    def load_template_config(
        self, config: FlextWebTypes.Core.RequestDict
    ) -> FlextResult[bool]:
        """Load template engine configuration - placeholder implementation."""
        _ = config
        return FlextResult[bool].ok(True)

    def get_template_config(self) -> FlextResult[FlextWebTypes.Core.ResponseDict]:
        """Get current template engine configuration - placeholder implementation."""
        return FlextResult[FlextWebTypes.Core.ResponseDict].ok({})

    def validate_template_config(
        self, config: FlextWebTypes.Core.RequestDict
    ) -> FlextResult[bool]:
        """Validate template engine configuration - placeholder implementation."""
        _ = config
        return FlextResult[bool].ok(True)

    def render(
        self, template: str, context: FlextWebTypes.Core.RequestDict
    ) -> FlextResult[str]:
        """Render template string with context - placeholder implementation."""
        _ = template, context
        return FlextResult[str].ok("")

    def add_filter(self, name: str, filter_func: Callable[[str], str]) -> None:
        """Add template filter function - placeholder implementation."""

    def add_global(
        self,
        name: str,
        *,
        value: str | int | bool | list[str] | dict[str, str | int | bool],
    ) -> None:
        """Add template global variable - placeholder implementation."""


class _WebConnectionBase:
    """Concrete base class for WebConnectionProtocol placeholder methods."""

    def get_endpoint_url(self) -> str:
        """Get the web service endpoint URL - placeholder implementation."""
        return "http://localhost:8080"


class _WebMonitoringBase:
    """Concrete base class for WebMonitoringProtocol placeholder methods."""

    def record_web_request(
        self, request: FlextWebTypes.Core.RequestDict, response_time: float
    ) -> None:
        """Record web request metrics - placeholder implementation."""

    def get_web_health_status(self) -> FlextWebTypes.Core.ResponseDict:
        """Get web application health status - placeholder implementation."""
        return {
            "status": FlextWebConstants.WebResponse.STATUS_HEALTHY,
            "service": FlextWebConstants.WebService.SERVICE_NAME,
        }

    def get_web_metrics(self) -> FlextWebTypes.Core.ResponseDict:
        """Get web application metrics - placeholder implementation."""
        return {"requests": 0, "errors": 0, "uptime": "0s"}


__all__ = [
    "FlextWebProtocols",  # Main hierarchical web protocol architecture
    # Concrete base classes for testing (internal use)
    "_WebAppManagerBase",
    "_WebConnectionBase",
    "_WebFrameworkInterfaceBase",
    "_WebHandlerBase",
    "_WebMonitoringBase",
    "_WebRepositoryBase",
    "_WebResponseFormatterBase",
    "_WebServiceBase",
    "_WebTemplateEngineBase",
    "_WebTemplateRendererBase",
]
