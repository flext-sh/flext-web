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
 Example: WebAppManagerProtocol extends p.Service[t.WebCore.ResponseDict]

USAGE IN WEB PROJECT:
 Web services extend FlextWebProtocols with web-specific protocols:

 >>> class WebAppService(FlextWebProtocols.Web.WebAppManagerProtocol):
... # Web-specific extensions
... pass

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

# NOTE(architecture): protocols.py contains ~1700 lines of implementation code.
# (servers, routes, middleware, test bases, metrics tracking). This violates
# architecture layers — protocols.py should contain ONLY Protocol definitions.
# Refactor implementation to separate modules in a future task.
# See: https://github.com/flext-sh/flext/issues/1

from __future__ import annotations

from collections.abc import Awaitable, Callable, Mapping
from copy import deepcopy
from threading import Thread
from time import sleep
from typing import ClassVar, Protocol, TypedDict, override, runtime_checkable
from uuid import uuid4

import flask
import uvicorn
from fastapi import FastAPI
from flext_core import FlextProtocols, FlextResult
from starlette.requests import Request as StarletteRequest
from starlette.responses import Response as StarletteResponse
from werkzeug.serving import BaseWSGIServer, make_server

from flext_web import FlextWebApp, c, m, t


class AppRuntimeInfo(TypedDict):
    """Typed structure for app runtime state."""

    runner: str
    server: uvicorn.Server | BaseWSGIServer
    thread: Thread


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

    2. Runtime Protocol Validation: runtime protocol checks validate
    implementations with the expected signatures

    3. Duck Typing Philosophy: "If it walks like a web app manager and manages
    like a web app manager, it's a web app manager"

    4. Metaclass Conflicts Prevented: @runtime_checkable protocols don't use
    ProtocolMeta with service metaclasses, avoiding inheritance conflicts

    5. Type Safety: Full mypy/pyright type checking without inheritance

    Example of structural typing:
    class Web:
        '''Satisfies FlextWebProtocols.Web.WebAppManagerProtocol through method implementation.'''
        def create_app(self, name: str, port: int, host: str) -> r:
            '''Required method - protocol compliance verified.'''
            pass

    service = WebApplicationService()
    # Runtime protocol validation succeeds for compliant implementations

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
    - WebAppManagerProtocol extends p.Service[t.WebCore.ResponseDict]
    - WebRepositoryProtocol extends p.Repository
    - Reduces duplication, improves maintainability

    **4. All web protocols are @runtime_checkable for runtime validation**
    - Runtime protocol checks validate compliance
    - Used for runtime type checking and validation in web components
    - Enables duck typing without metaclass conflicts

    EXTENSION PATTERN - HOW WEB PROJECTS USE p

    Web projects extend FlextWebProtocols with domain-specific protocols:

    **Example 1: Web Application Project**
    # (See actual implementation above for correct usage patterns)

    **Example 2: Web API Project**
    # (See actual implementation above for correct usage patterns)
                    ...

    INTEGRATION POINTS WITH FLEXT WEB ARCHITECTURE

    r Integration:
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
    Performance: runtime protocol checks optimized for production use

    CORE PRINCIPLES:
        1. Web protocols extend p with web-specific interfaces
        2. Web protocols live in their respective web projects
        3. Protocol inheritance creates logical web hierarchies
        4. All web protocols are @runtime_checkable for runtime validation

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

        @runtime_checkable
        class FastApiLikeApp(Protocol):
            """Duck-type protocol for FastAPI-like framework apps."""

            def add_api_route(
                self,
                path: str,
                endpoint: Callable[..., t.WebCore.ResponseDict],
                **kwargs: t.GeneralValueType,
            ) -> None:
                """Register an API route."""
                ...

            def middleware(
                self, middleware_type: str
            ) -> Callable[..., Callable[..., StarletteResponse]]:
                """Register middleware."""
                ...

        @runtime_checkable
        class FlaskLikeApp(Protocol):
            """Duck-type protocol for Flask-like framework apps."""

            def route(
                self, rule: str, **options: t.GeneralValueType
            ) -> Callable[..., Callable[..., t.WebCore.ResponseDict]]:
                """Register a URL route."""
                ...

            def before_request(self, f: Callable[..., None]) -> Callable[..., None]:
                """Register a before-request hook."""
                ...

        apps_registry: ClassVar[dict[str, t.WebCore.ResponseDict]] = {}
        framework_instances: ClassVar[dict[str, flask.Flask | FastAPI]] = {}
        app_runtimes: ClassVar[dict[str, AppRuntimeInfo]] = {}
        service_state: ClassVar[dict[str, bool]] = {
            "routes_initialized": False,
            "middleware_configured": False,
            "service_running": False,
        }
        web_metrics: ClassVar[dict[str, int | str]] = {}
        template_config: ClassVar[t.WebCore.RequestDict] = {}
        template_globals: ClassVar[dict[str, t.GeneralValueType]] = {}
        template_filters: ClassVar[dict[str, Callable[[str], str]]] = {}

        @staticmethod
        def _is_valid_port(port: int) -> bool:
            min_port, max_port = c.Web.WebValidation.PORT_RANGE
            return min_port <= port <= max_port

        @classmethod
        def _create_framework_app(
            cls,
            name: str,
        ) -> FlextResult[tuple[flask.Flask | FastAPI, str, str]]:
            fastapi_result = FlextWebApp.create_fastapi_app(
                config=m.Web.FastAPIAppConfig(title=name),
            )
            if fastapi_result.is_success:
                return FlextResult[tuple[flask.Flask | FastAPI, str, str]].ok(
                    (
                        fastapi_result.value,
                        c.Web.WebFramework.FRAMEWORK_FASTAPI,
                        c.Web.WebFramework.INTERFACE_ASGI,
                    ),
                )

            flask_result = FlextWebApp.create_flask_app()
            if flask_result.is_success:
                return FlextResult[tuple[flask.Flask | FastAPI, str, str]].ok(
                    (
                        flask_result.value,
                        c.Web.WebFramework.FRAMEWORK_FLASK,
                        c.Web.WebFramework.INTERFACE_WSGI,
                    ),
                )

            return FlextResult[tuple[flask.Flask | FastAPI, str, str]].fail(
                fastapi_result.error
                if fastapi_result.error is not None
                else "Failed to create web framework application",
            )

        @staticmethod
        def _copy_response_dict(
            data: t.WebCore.RequestDict | t.WebCore.ResponseDict,
        ) -> t.WebCore.ResponseDict:
            return deepcopy(data)

        @staticmethod
        def _record_request_metric(status: str | None, response_time_ms: int) -> None:
            request_count_value = FlextWebProtocols.Web.web_metrics.get("requests", 0)
            request_count = (
                request_count_value if isinstance(request_count_value, int) else 0
            )
            next_count = request_count + 1
            FlextWebProtocols.Web.web_metrics["requests"] = next_count

            avg_value = FlextWebProtocols.Web.web_metrics.get("avg_response_time_ms", 0)
            previous_avg = avg_value if isinstance(avg_value, int) else 0
            average_response_time_ms = (
                (previous_avg * request_count) + response_time_ms
            ) / next_count
            FlextWebProtocols.Web.web_metrics["avg_response_time_ms"] = int(
                average_response_time_ms,
            )

            if (
                isinstance(status, str)
                and status.lower() == c.Web.WebResponse.STATUS_ERROR
            ):
                error_count_value = FlextWebProtocols.Web.web_metrics.get("errors", 0)
                error_count = (
                    error_count_value if isinstance(error_count_value, int) else 0
                )
                FlextWebProtocols.Web.web_metrics["errors"] = error_count + 1

        @staticmethod
        def _configure_framework_app_routes(
            app_instance: flask.Flask | FastAPI, app_id: str
        ) -> None:
            if isinstance(app_instance, FlextWebProtocols.Web.FastApiLikeApp):
                route_registrar = app_instance.add_api_route

                def fastapi_health() -> t.WebCore.ResponseDict:
                    return {
                        "status": c.Web.WebResponse.STATUS_HEALTHY,
                        "service": c.Web.WebService.SERVICE_NAME,
                        "app_id": app_id,
                    }

                route_registrar("/protocol/health", fastapi_health, methods=["GET"])

            if isinstance(app_instance, FlextWebProtocols.Web.FlaskLikeApp):
                route_decorator = app_instance.route

                @route_decorator("/protocol/health")
                def flask_health() -> t.WebCore.ResponseDict:
                    return {
                        "status": c.Web.WebResponse.STATUS_HEALTHY,
                        "service": c.Web.WebService.SERVICE_NAME_FLASK,
                        "app_id": app_id,
                    }

        @staticmethod
        def _configure_framework_app_middleware(
            app_instance: flask.Flask | FastAPI,
        ) -> None:
            if isinstance(app_instance, FlextWebProtocols.Web.FastApiLikeApp):
                middleware_decorator = app_instance.middleware

                @middleware_decorator("http")
                async def fastapi_metrics_middleware(
                    request: StarletteRequest,
                    call_next: Callable[
                        [StarletteRequest], Awaitable[StarletteResponse]
                    ],
                ) -> StarletteResponse:
                    response = call_next(request)
                    if isinstance(response, Awaitable):
                        response = await response
                    FlextWebProtocols.Web.record_request_metric("success", 0)
                    return response

            if isinstance(app_instance, FlextWebProtocols.Web.FlaskLikeApp):

                @app_instance.before_request
                def flask_metrics_middleware() -> None:
                    FlextWebProtocols.Web.record_request_metric("success", 0)

        @staticmethod
        def _start_app_runtime(
            app_id: str,
            app_data: t.WebCore.ResponseDict,
            app_instance: flask.Flask | FastAPI,
        ) -> FlextResult[AppRuntimeInfo]:
            host = app_data.get("host")
            port = app_data.get("port")
            interface = app_data.get("interface")
            if not isinstance(host, str) or not isinstance(port, int):
                return FlextResult[AppRuntimeInfo].fail(
                    f"Invalid runtime configuration for app: {app_id}",
                )

            if interface == c.Web.WebFramework.INTERFACE_ASGI:
                try:
                    config = uvicorn.Config(
                        app=app_instance,
                        host=host,
                        port=port,
                        log_level="warning",
                    )
                    server = uvicorn.Server(config)
                    thread = Thread(
                        target=server.run, daemon=True, name=f"flext-web-{app_id}"
                    )
                    thread.start()
                    sleep(0.05)
                    if not thread.is_alive():
                        return FlextResult[AppRuntimeInfo].fail(
                            f"ASGI runtime exited immediately for app: {app_id}",
                        )
                    return FlextResult[AppRuntimeInfo].ok({
                        "runner": c.Web.WebFramework.RUNNER_UVICORN,
                        "server": server,
                        "thread": thread,
                    })
                except (RuntimeError, OSError, ValueError, TypeError) as exc:
                    return FlextResult[AppRuntimeInfo].fail(
                        f"Failed to start ASGI runtime for app {app_id}: {exc}",
                    )

            if interface == c.Web.WebFramework.INTERFACE_WSGI and isinstance(
                app_instance, flask.Flask
            ):
                try:
                    wsgi_server = make_server(host, port, app_instance)
                    thread = Thread(
                        target=wsgi_server.serve_forever,
                        daemon=True,
                        name=f"flext-web-{app_id}",
                    )
                    thread.start()
                    sleep(0.05)
                    if not thread.is_alive():
                        return FlextResult[AppRuntimeInfo].fail(
                            f"WSGI runtime exited immediately for app: {app_id}",
                        )
                    return FlextResult[AppRuntimeInfo].ok({
                        "runner": c.Web.WebFramework.RUNNER_WERKZEUG,
                        "server": wsgi_server,
                        "thread": thread,
                    })
                except (
                    RuntimeError,
                    OSError,
                    ValueError,
                    TypeError,
                    AttributeError,
                ) as exc:
                    return FlextResult[AppRuntimeInfo].fail(
                        f"Failed to start WSGI runtime for app {app_id}: {exc}",
                    )

            return FlextResult[AppRuntimeInfo].fail(
                f"Unsupported app interface for runtime start: {interface}",
            )

        @staticmethod
        def _stop_app_runtime(
            app_id: str, runtime: AppRuntimeInfo
        ) -> FlextResult[bool]:
            runner = runtime.get("runner")
            server = runtime.get("server")
            thread = runtime.get("thread")
            if not isinstance(thread, Thread):
                return FlextResult[bool].fail(
                    f"Missing runtime thread for app: {app_id}"
                )

            try:
                if runner == c.Web.WebFramework.RUNNER_UVICORN:
                    if not isinstance(server, uvicorn.Server):
                        return FlextResult[bool].fail(
                            f"Missing ASGI server instance for app: {app_id}"
                        )
                    server.should_exit = True
                elif runner == c.Web.WebFramework.RUNNER_WERKZEUG:
                    if not isinstance(server, BaseWSGIServer):
                        return FlextResult[bool].fail(
                            f"Missing WSGI server instance for app: {app_id}"
                        )
                    server.shutdown()
                    server.server_close()
                else:
                    return FlextResult[bool].fail(
                        f"Unsupported runtime runner for app: {app_id}"
                    )

                thread.join(timeout=2.0)
                if thread.is_alive():
                    return FlextResult[bool].fail(
                        f"Runtime thread did not stop cleanly for app: {app_id}",
                    )
            except (RuntimeError, AttributeError, OSError) as exc:
                return FlextResult[bool].fail(
                    f"Failed to stop app runtime {app_id}: {exc}",
                )

            return FlextResult[bool].ok(True)

        # Public aliases for private methods
        record_request_metric: ClassVar[Callable[..., None]] = _record_request_metric
        create_framework_app: ClassVar[
            Callable[..., FlextResult[tuple[flask.Flask | FastAPI, str, str]]]
        ] = _create_framework_app
        copy_response_dict: ClassVar[Callable[..., t.WebCore.ResponseDict]] = (
            _copy_response_dict
        )
        configure_framework_app_routes: ClassVar[Callable[..., None]] = (
            _configure_framework_app_routes
        )
        configure_framework_app_middleware: ClassVar[Callable[..., None]] = (
            _configure_framework_app_middleware
        )
        start_app_runtime: ClassVar[Callable[..., FlextResult[AppRuntimeInfo]]] = (
            _start_app_runtime
        )
        stop_app_runtime: ClassVar[Callable[..., FlextResult[bool]]] = _stop_app_runtime
        is_valid_port: ClassVar[Callable[[int], bool]] = _is_valid_port

        # =========================================================================
        # WEB FOUNDATION LAYER - Core web protocols used within flext-web
        # =========================================================================

        @runtime_checkable
        class WebAppManagerProtocol(
            FlextProtocols.Service[t.WebCore.ResponseDict], Protocol
        ):
            """Protocol for web application lifecycle management.

            Extends p.Service[t.WebCore.ResponseDict] with web-specific application management
            operations. Provides standardized interface for creating, starting, stopping,
            and managing web applications.

            Used in: handlers.py (FlextWebHandlers.ApplicationHandler)
            """

            @staticmethod
            def create_app(
                name: str,
                port: int,
                host: str,
            ) -> FlextResult[t.WebCore.ResponseDict]:
                """Create a new web application.

                Args:
                    name: Application name identifier
                    port: Network port for the application
                    host: Network host address for binding

                Returns:
                    r containing application data or error details

                """
                if len(name.strip()) < c.Web.WebServer.MIN_APP_NAME_LENGTH:
                    return FlextResult[t.WebCore.ResponseDict].fail(
                        f"Application name must be at least {c.Web.WebServer.MIN_APP_NAME_LENGTH} characters",
                    )
                if not host.strip():
                    return FlextResult[t.WebCore.ResponseDict].fail(
                        "Host cannot be empty"
                    )
                if not FlextWebProtocols.Web.is_valid_port(port):
                    min_port, max_port = c.Web.WebValidation.PORT_RANGE
                    return FlextResult[t.WebCore.ResponseDict].fail(
                        f"Port must be between {min_port} and {max_port}",
                    )

                framework_result = FlextWebProtocols.Web.create_framework_app(name)
                if framework_result.is_failure:
                    return FlextResult[t.WebCore.ResponseDict].fail(
                        framework_result.error
                    )

                app_instance, framework_name, interface_type = framework_result.value
                app_id = str(uuid4())
                FlextWebProtocols.Web.configure_framework_app_routes(
                    app_instance, app_id
                )
                FlextWebProtocols.Web.configure_framework_app_middleware(app_instance)
                app_data: t.WebCore.ResponseDict = {
                    "id": app_id,
                    "name": name,
                    "port": port,
                    "host": host,
                    "status": c.Web.Status.STOPPED.value,
                    "framework": framework_name,
                    "interface": interface_type,
                }
                FlextWebProtocols.Web.apps_registry[app_id] = app_data
                FlextWebProtocols.Web.framework_instances[app_id] = app_instance
                return FlextResult[t.WebCore.ResponseDict].ok(app_data)

            @staticmethod
            def start_app(
                app_id: str,
            ) -> FlextResult[t.WebCore.ResponseDict]:
                """Start a web application.

                Args:
                app_id: Unique identifier of the application to start

                Returns:
                r containing start operation result or error details

                """
                app_data = FlextWebProtocols.Web.apps_registry.get(app_id)
                if app_data is None:
                    return FlextResult[t.WebCore.ResponseDict].fail(
                        f"Application not found: {app_id}",
                    )
                if app_data.get("status") == c.Web.Status.RUNNING.value:
                    return FlextResult[t.WebCore.ResponseDict].fail(
                        f"Application already running: {app_id}",
                    )

                app_instance = FlextWebProtocols.Web.framework_instances.get(app_id)
                if app_instance is None:
                    return FlextResult[t.WebCore.ResponseDict].fail(
                        f"Application runtime instance not found: {app_id}",
                    )

                runtime_result = FlextWebProtocols.Web.start_app_runtime(
                    app_id,
                    app_data,
                    app_instance,
                )
                if runtime_result.is_failure:
                    return FlextResult[t.WebCore.ResponseDict].fail(
                        runtime_result.error
                    )

                updated_app = FlextWebProtocols.Web.copy_response_dict(app_data)
                updated_app["status"] = c.Web.Status.RUNNING.value
                FlextWebProtocols.Web.apps_registry[app_id] = updated_app
                FlextWebProtocols.Web.app_runtimes[app_id] = runtime_result.value
                return FlextResult[t.WebCore.ResponseDict].ok(updated_app)

            @staticmethod
            def stop_app(
                app_id: str,
            ) -> FlextResult[t.WebCore.ResponseDict]:
                """Stop a running web application.

                Args:
                app_id: Unique identifier of the application to stop

                Returns:
                r containing stop operation result or error details

                """
                app_data = FlextWebProtocols.Web.apps_registry.get(app_id)
                if app_data is None:
                    return FlextResult[t.WebCore.ResponseDict].fail(
                        f"Application not found: {app_id}",
                    )
                if app_data.get("status") != c.Web.Status.RUNNING.value:
                    return FlextResult[t.WebCore.ResponseDict].fail(
                        f"Application not running: {app_id}",
                    )

                runtime = FlextWebProtocols.Web.app_runtimes.get(app_id)
                if runtime is None:
                    return FlextResult[t.WebCore.ResponseDict].fail(
                        f"Application runtime not found for stop: {app_id}",
                    )

                stop_runtime_result = FlextWebProtocols.Web.stop_app_runtime(
                    app_id, runtime
                )
                if stop_runtime_result.is_failure:
                    return FlextResult[t.WebCore.ResponseDict].fail(
                        stop_runtime_result.error
                    )

                updated_app = FlextWebProtocols.Web.copy_response_dict(app_data)
                updated_app["status"] = c.Web.Status.STOPPED.value
                FlextWebProtocols.Web.apps_registry[app_id] = updated_app
                _ = FlextWebProtocols.Web.app_runtimes.pop(app_id, None)
                return FlextResult[t.WebCore.ResponseDict].ok(updated_app)

            @staticmethod
            def list_apps() -> FlextResult[list[t.WebCore.ResponseDict]]:
                """List all web applications.

                Returns:
                r containing list of application data or error details

                """
                apps = [
                    FlextWebProtocols.Web.copy_response_dict(app)
                    for app in FlextWebProtocols.Web.apps_registry.values()
                ]
                return FlextResult[list[t.WebCore.ResponseDict]].ok(apps)

        @runtime_checkable
        class WebResponseFormatterProtocol(
            FlextProtocols.Service[t.WebCore.ResponseDict],
            Protocol,
        ):
            """Protocol for web response formatting.

            Extends p.Service[t.WebCore.ResponseDict] with web-specific response formatting
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
                response: t.WebCore.ResponseDict = {
                    "status": c.Web.WebResponse.STATUS_SUCCESS,
                }
                response.update(FlextWebProtocols.Web.copy_response_dict(data))
                return response

            @staticmethod
            def format_error(error: Exception) -> t.WebCore.ResponseDict:
                """Format error response data.

                Args:
                error: Exception to format as error response

                Returns:
                Formatted error response dictionary

                """
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
                response: t.WebCore.ResponseDict = {
                    c.Web.Http.HEADER_CONTENT_TYPE: c.Web.Http.CONTENT_TYPE_JSON,
                }
                response.update(FlextWebProtocols.Web.copy_response_dict(data))
                return response

            @staticmethod
            def get_request_data(
                _request: t.WebCore.RequestDict,
            ) -> t.WebCore.RequestDict:
                """Extract data from web request.

                Args:
                _request: Web request data

                Returns:
                Extracted request data dictionary

                """
                return deepcopy(_request)

        @runtime_checkable
        class WebFrameworkInterfaceProtocol(
            FlextProtocols.Service[t.WebCore.ResponseDict],
            Protocol,
        ):
            """Protocol for web framework integration.

            Extends p.Service[t.WebCore.ResponseDict] with web framework integration operations.
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
                response: t.WebCore.ResponseDict = {
                    c.Web.Http.HEADER_CONTENT_TYPE: c.Web.Http.CONTENT_TYPE_JSON,
                }
                response.update(FlextWebProtocols.Web.copy_response_dict(data))
                return response

            @staticmethod
            def get_request_data(
                _request: t.WebCore.RequestDict,
            ) -> t.WebCore.RequestDict:
                """Extract data from web request.

                Args:
                _request: Web request data

                Returns:
                Extracted request data dictionary

                """
                return deepcopy(_request)

            @staticmethod
            def is_json_request(_request: t.WebCore.RequestDict) -> bool:
                """Check if request contains JSON data.

                Args:
                _request: Web request to check

                Returns:
                True if request is JSON, False otherwise

                """
                content_type = _request.get(c.Web.Http.HEADER_CONTENT_TYPE)
                if isinstance(content_type, str):
                    return c.Web.Http.CONTENT_TYPE_JSON in content_type.lower()

                headers = _request.get("headers")
                if isinstance(headers, dict):
                    nested_content_type = headers.get(c.Web.Http.HEADER_CONTENT_TYPE)
                    if isinstance(nested_content_type, str):
                        return (
                            c.Web.Http.CONTENT_TYPE_JSON in nested_content_type.lower()
                        )

                return False

        # =========================================================================
        # WEB DOMAIN LAYER - Web service and repository protocols
        # =========================================================================

        @runtime_checkable
        class WebServiceProtocol(
            FlextProtocols.Service[t.WebCore.ResponseDict], Protocol
        ):
            """Base web service protocol.

            Extends p.Service[t.WebCore.ResponseDict] with web-specific service operations.
            Provides the foundation for all web services in the FLEXT web ecosystem.

            Used in: web service implementations
            """

            @staticmethod
            def initialize_routes() -> FlextResult[bool]:
                """Initialize web service routes.

                Returns:
                FlextResult[bool]: Success contains True if routes initialized, failure with error details

                """
                FlextWebProtocols.Web.service_state["routes_initialized"] = True
                return FlextResult[bool].ok(value=True)

            @staticmethod
            def configure_middleware() -> FlextResult[bool]:
                """Configure web service middleware.

                Returns:
                FlextResult[bool]: Success contains True if middleware configured, failure with error details

                """
                FlextWebProtocols.Web.service_state["middleware_configured"] = True
                return FlextResult[bool].ok(value=True)

            @staticmethod
            def start_service() -> FlextResult[bool]:
                """Start the web service.

                Returns:
                FlextResult[bool]: Success contains True if service started, failure with error details

                """
                state = FlextWebProtocols.Web.service_state
                if not state["routes_initialized"]:
                    return FlextResult[bool].fail(
                        "Routes must be initialized before starting service"
                    )
                if not state["middleware_configured"]:
                    return FlextResult[bool].fail(
                        "Middleware must be configured before starting service"
                    )
                if state["service_running"]:
                    return FlextResult[bool].fail("Service is already running")
                state["service_running"] = True
                return FlextResult[bool].ok(value=True)

            @staticmethod
            def stop_service() -> FlextResult[bool]:
                """Stop the web service.

                Returns:
                FlextResult[bool]: Success contains True if service stopped, failure with error details

                """
                state = FlextWebProtocols.Web.service_state
                if not state["service_running"]:
                    return FlextResult[bool].fail("Service is not running")
                state["service_running"] = False
                return FlextResult[bool].ok(value=True)

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
            ) -> FlextResult[list[t.WebCore.ResponseDict]]:
                """Find entities by criteria.

                Args:
                criteria: Search criteria dictionary

                Returns:
                r containing list of matching entities or error details

                """
                matches: list[t.WebCore.ResponseDict] = []
                for app_data in FlextWebProtocols.Web.apps_registry.values():
                    is_match = True
                    for key, expected_value in criteria.items():
                        if app_data.get(key) != expected_value:
                            is_match = False
                            break
                    if is_match:
                        matches.append(
                            FlextWebProtocols.Web.copy_response_dict(app_data)
                        )

                return FlextResult[list[t.WebCore.ResponseDict]].ok(matches)

        # =========================================================================
        # WEB APPLICATION LAYER - Web handler and command patterns
        # =========================================================================

        @runtime_checkable
        class WebHandlerProtocol(
            FlextProtocols.Handler[t.WebCore.RequestDict, t.WebCore.ResponseDict],
            Protocol,
        ):
            """Web handler protocol for request/response patterns.

            Extends p.Handler with web-specific handler operations.
            Provides standardized interface for web request handling.

            Used in: web request handlers and controllers
            """

            def execute(
                self,
                command: t.WebCore.RequestDict,
            ) -> FlextResult[t.WebCore.ResponseDict]:
                """Execute command (extends p.Handler pattern).

                Args:
                    command: Command to execute

                Returns:
                    r containing response data or error details

                """
                return FlextWebProtocols.Web.WebHandlerProtocol.handle_request(command)

            @staticmethod
            def handle_request(
                request: t.WebCore.RequestDict,
            ) -> FlextResult[t.WebCore.ResponseDict]:
                """Handle web request and return response.

                Args:
                request: Web request data

                Returns:
                r containing response data or error details

                """
                action = request.get("action")
                if action == c.Web.WebActions.ACTION_CREATE:
                    name = request.get("name")
                    port = request.get("port")
                    host = request.get("host")
                    if (
                        not isinstance(name, str)
                        or not isinstance(port, int)
                        or not isinstance(host, str)
                    ):
                        return FlextResult[t.WebCore.ResponseDict].fail(
                            "create action requires name(str), port(int), host(str)",
                        )
                    return FlextWebProtocols.Web.WebAppManagerProtocol.create_app(
                        name=name,
                        port=port,
                        host=host,
                    )
                if action == c.Web.WebActions.ACTION_START:
                    app_id = request.get("app_id")
                    if not isinstance(app_id, str):
                        return FlextResult[t.WebCore.ResponseDict].fail(
                            "start action requires app_id(str)"
                        )
                    return FlextWebProtocols.Web.WebAppManagerProtocol.start_app(app_id)
                if action == c.Web.WebActions.ACTION_STOP:
                    app_id = request.get("app_id")
                    if not isinstance(app_id, str):
                        return FlextResult[t.WebCore.ResponseDict].fail(
                            "stop action requires app_id(str)"
                        )
                    return FlextWebProtocols.Web.WebAppManagerProtocol.stop_app(app_id)
                if action == c.Web.WebActions.ACTION_LIST:
                    return FlextWebProtocols.Web.WebAppManagerProtocol.list_apps().map(
                        lambda apps: {
                            "count": len(apps),
                            "app_ids": [
                                app_id
                                for app in apps
                                for app_id in [app.get("id")]
                                if isinstance(app_id, str)
                            ],
                        },
                    )

                return FlextResult[t.WebCore.ResponseDict].ok(
                    FlextWebProtocols.Web.copy_response_dict(request)
                )

        # =========================================================================
        # WEB INFRASTRUCTURE LAYER - Web external integrations
        # =========================================================================

        @runtime_checkable
        class WebConnectionProtocol(
            FlextProtocols.Service[t.WebCore.ResponseDict], Protocol
        ):
            """Web connection protocol for external systems.

            Extends p.Service[t.WebCore.ResponseDict] with web-specific connection operations.
            Provides standardized interface for web service connections.

            Used in: web service adapters and external integrations
            """

            @staticmethod
            def get_endpoint_url() -> str:
                """Get the web service endpoint URL.

                Returns:
                Web service endpoint URL string

                """
                running_apps = [
                    app
                    for app in FlextWebProtocols.Web.apps_registry.values()
                    if app.get("status") == c.Web.Status.RUNNING.value
                ]
                target_app = running_apps[0] if running_apps else None
                if target_app is None:
                    return "http://localhost:8080"

                host = target_app.get("host")
                port = target_app.get("port")
                if isinstance(host, str) and isinstance(port, int):
                    return f"http://{host}:{port}"

                return "http://localhost:8080"

        @runtime_checkable
        class WebLoggerProtocol(
            FlextProtocols.Service[t.WebCore.ResponseDict], Protocol
        ):
            """Web logging protocol.

            Extends p.Service[t.WebCore.ResponseDict] with web-specific logging operations.
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
                merged_status = None
                if isinstance(context, dict):
                    context_status = context.get("status")
                    if isinstance(context_status, str):
                        merged_status = context_status
                request_status = request.get("status")
                if isinstance(request_status, str):
                    merged_status = request_status
                FlextWebProtocols.Web.record_request_metric(merged_status, 0)

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
                merged_status = None
                if isinstance(context, dict):
                    context_status = context.get("status")
                    if isinstance(context_status, str):
                        merged_status = context_status
                response_status = response.get("status")
                if isinstance(response_status, str):
                    merged_status = response_status
                FlextWebProtocols.Web.record_request_metric(merged_status, 0)

        # =========================================================================
        # WEB TEMPLATE LAYER - Template rendering protocols
        # =========================================================================

        @runtime_checkable
        class WebTemplateRendererProtocol(
            FlextProtocols.Service[t.WebCore.ResponseDict],
            Protocol,
        ):
            """Protocol for web template rendering.

            Extends p.Service[t.WebCore.ResponseDict] with web template rendering operations.
            Provides standardized interface for template engine integration.

            Used in: web template rendering implementations
            """

            @staticmethod
            def render_template(
                template_name: str,
                context: t.WebCore.RequestDict,
            ) -> FlextResult[str]:
                """Render template with context data.

                Args:
                template_name: Name of the template to render
                context: Template context data

                Returns:
                r containing rendered template string or error details

                """
                rendered = template_name
                for key, value in context.items():
                    if isinstance(value, (str, int, bool)):
                        rendered = rendered.replace(f"{{{{{key}}}}}", str(value))
                return FlextResult[str].ok(rendered)

            @staticmethod
            def render_dashboard(
                data: t.WebCore.ResponseDict,
            ) -> FlextResult[str]:
                """Render dashboard template with data.

                Args:
                data: Dashboard data to render

                Returns:
                r containing rendered dashboard HTML or error details

                """
                app_name = data.get("service", c.Web.WebService.SERVICE_NAME)
                status = data.get("status", c.Web.Status.STOPPED.value)
                html = (
                    "<html><body>"
                    f"<h1>{app_name}</h1>"
                    f"<p>Status: {status}</p>"
                    "</body></html>"
                )
                return FlextResult[str].ok(html)

        @runtime_checkable
        class WebTemplateEngineProtocol(
            FlextProtocols.Service[t.WebCore.ResponseDict],
            Protocol,
        ):
            """Protocol for web template engine operations.

            Extends p.Service[t.WebCore.ResponseDict] with template engine management operations.
            Provides interface for loading, validating, and managing templates.

            Used in: web template engine implementations
            """

            @staticmethod
            def load_template_config(
                config: t.WebCore.RequestDict,
            ) -> FlextResult[bool]:
                """Load template engine configuration.

                Args:
                config: Template engine configuration

                Returns:
                FlextResult[bool]: Success contains True if config loaded, failure with error details

                """
                FlextWebProtocols.Web.template_config = deepcopy(config)
                return FlextResult[bool].ok(value=True)

            @staticmethod
            def get_template_config() -> FlextResult[t.WebCore.ResponseDict]:
                """Get current template engine configuration.

                Returns:
                r containing configuration data or error details

                """
                return FlextResult[t.WebCore.ResponseDict].ok(
                    FlextWebProtocols.Web.copy_response_dict(
                        FlextWebProtocols.Web.template_config,
                    ),
                )

            @staticmethod
            def validate_template_config(
                config: t.WebCore.RequestDict,
            ) -> FlextResult[bool]:
                """Validate template engine configuration.

                Args:
                config: Configuration to validate

                Returns:
                FlextResult[bool]: Success contains True if valid, failure with error details

                """
                allowed_keys = {"template_dir", "autoescape", "cache_enabled"}
                invalid_keys = [key for key in config if key not in allowed_keys]
                if invalid_keys:
                    return FlextResult[bool].fail(
                        f"Invalid template config keys: {', '.join(invalid_keys)}",
                    )
                return FlextResult[bool].ok(value=True)

            @staticmethod
            def render(
                template: str,
                context: t.WebCore.RequestDict,
            ) -> FlextResult[str]:
                """Render template string with context.

                Args:
                template: Template string to render
                context: Template context data

                Returns:
                r containing rendered template or error details

                """
                full_context = deepcopy(FlextWebProtocols.Web.template_globals)
                full_context.update(context)

                rendered = template
                for key, value in full_context.items():
                    if isinstance(value, (str, int, bool)):
                        rendered = rendered.replace(f"{{{{{key}}}}}", str(value))

                for (
                    filter_name,
                    filter_fn,
                ) in FlextWebProtocols.Web.template_filters.items():
                    marker = f"|{filter_name}"
                    if marker in rendered:
                        rendered = filter_fn(rendered.replace(marker, ""))

                return FlextResult[str].ok(rendered)

            def add_filter(self, name: str, filter_func: Callable[[str], str]) -> None:
                """Add template filter function.

                Args:
                name: Filter name identifier
                filter_func: Filter function implementation

                """
                FlextWebProtocols.Web.template_filters[name] = filter_func

            def add_global(
                self,
                name: str,
                *,
                value: t.GeneralValueType,
            ) -> None:
                """Add template global variable.

                Args:
                name: Global variable name
                value: Global variable value

                """
                FlextWebProtocols.Web.template_globals[name] = (
                    dict(value) if isinstance(value, Mapping) else value
                )

        # =========================================================================
        # WEB MONITORING LAYER - Observability and monitoring protocols
        # =========================================================================

        @runtime_checkable
        class WebMonitoringProtocol(
            FlextProtocols.Service[t.WebCore.ResponseDict], Protocol
        ):
            """Web monitoring protocol for observability.

            Extends p.Service[t.WebCore.ResponseDict] with web-specific monitoring operations.
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
                status_value = request.get("status")
                status = status_value if isinstance(status_value, str) else None
                response_time_ms = int(max(response_time, 0) * 1000)
                FlextWebProtocols.Web.record_request_metric(status, response_time_ms)

            @staticmethod
            def get_web_health_status() -> t.WebCore.ResponseDict:
                """Get web application health status.

                Returns:
                Health status information dictionary

                """
                service_running = FlextWebProtocols.Web.service_state["service_running"]
                return {
                    "status": (
                        c.Web.WebResponse.STATUS_HEALTHY
                        if service_running
                        else c.Web.Status.STOPPED.value
                    ),
                    "service": c.Web.WebService.SERVICE_NAME,
                    "routes_initialized": FlextWebProtocols.Web.service_state[
                        "routes_initialized"
                    ],
                    "middleware_configured": FlextWebProtocols.Web.service_state[
                        "middleware_configured"
                    ],
                }

            @staticmethod
            def get_web_metrics() -> t.WebCore.ResponseDict:
                """Get web application metrics.

                Returns:
                Web metrics data dictionary

                """
                metrics: t.WebCore.ResponseDict = {}
                for key, val in FlextWebProtocols.Web.web_metrics.items():
                    metrics[key] = int(val) if isinstance(val, float) else val
                return metrics

        @runtime_checkable
        class ConfigValueProtocol(Protocol):
            """Protocol for configuration values."""

            value: t.ScalarValue

            @override
            def __str__(self) -> str:
                """Convert to string."""
                return str(self.value) if self.value is not None else ""

            def __int__(self) -> int:
                """Convert to integer."""
                if self.value is None:
                    return 0
                try:
                    return int(self.value)
                except (ValueError, TypeError):
                    return 0

            def __bool__(self) -> bool:
                """Convert to boolean."""
                return bool(self.value) if self.value is not None else False

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
        class TestBases:
            """Namespace for test base implementations."""

            class _WebAppManagerBase:
                """Base implementation of WebAppManagerProtocol for testing."""

                def create_app(
                    self,
                    name: str,
                    port: int,
                    host: str,
                ) -> FlextResult[t.WebCore.ResponseDict]:
                    """Create a new web application."""
                    return FlextWebProtocols.Web.WebAppManagerProtocol.create_app(
                        name, port, host
                    )

                def start_app(self, app_id: str) -> FlextResult[t.WebCore.ResponseDict]:
                    """Start a web application."""
                    return FlextWebProtocols.Web.WebAppManagerProtocol.start_app(app_id)

                def stop_app(self, app_id: str) -> FlextResult[t.WebCore.ResponseDict]:
                    """Stop a running web application."""
                    return FlextWebProtocols.Web.WebAppManagerProtocol.stop_app(app_id)

                def list_apps(
                    self,
                ) -> FlextResult[list[t.WebCore.ResponseDict]]:
                    """List all web applications."""
                    return FlextWebProtocols.Web.WebAppManagerProtocol.list_apps()

            class _WebResponseFormatterBase:
                """Base implementation of WebResponseFormatterProtocol for testing."""

                def format_success(
                    self, data: t.WebCore.ResponseDict
                ) -> t.WebCore.ResponseDict:
                    """Format successful response data."""
                    return FlextWebProtocols.Web.WebResponseFormatterProtocol.format_success(
                        data
                    )

                def format_error(self, error: Exception) -> t.WebCore.ResponseDict:
                    """Format error response data."""
                    return (
                        FlextWebProtocols.Web.WebResponseFormatterProtocol.format_error(
                            error
                        )
                    )

                def create_json_response(
                    self,
                    data: t.WebCore.ResponseDict,
                ) -> t.WebCore.ResponseDict:
                    """Create a JSON response."""
                    return FlextWebProtocols.Web.WebResponseFormatterProtocol.create_json_response(
                        data
                    )

                def get_request_data(
                    self,
                    _request: t.WebCore.RequestDict,
                ) -> t.WebCore.RequestDict:
                    """Extract data from web request."""
                    return FlextWebProtocols.Web.WebResponseFormatterProtocol.get_request_data(
                        _request
                    )

            class _WebFrameworkInterfaceBase:
                """Base implementation of WebFrameworkInterfaceProtocol for testing."""

                def create_json_response(
                    self,
                    data: t.WebCore.ResponseDict,
                ) -> t.WebCore.ResponseDict:
                    """Create a JSON response."""
                    return FlextWebProtocols.Web.WebFrameworkInterfaceProtocol.create_json_response(
                        data,
                    )

                def get_request_data(
                    self,
                    _request: t.WebCore.RequestDict,
                ) -> t.WebCore.RequestDict:
                    """Extract data from web request."""
                    return FlextWebProtocols.Web.WebFrameworkInterfaceProtocol.get_request_data(
                        _request,
                    )

                def is_json_request(self, _request: t.WebCore.RequestDict) -> bool:
                    """Check if request contains JSON data."""
                    return FlextWebProtocols.Web.WebFrameworkInterfaceProtocol.is_json_request(
                        _request
                    )

            class _WebServiceBase:
                """Base implementation of WebServiceProtocol for testing."""

                def initialize_routes(self) -> FlextResult[bool]:
                    """Initialize web service routes."""
                    return FlextWebProtocols.Web.WebServiceProtocol.initialize_routes()

                def configure_middleware(self) -> FlextResult[bool]:
                    """Configure web service middleware."""
                    return (
                        FlextWebProtocols.Web.WebServiceProtocol.configure_middleware()
                    )

                def start_service(self) -> FlextResult[bool]:
                    """Start the web service."""
                    return FlextWebProtocols.Web.WebServiceProtocol.start_service()

                def stop_service(self) -> FlextResult[bool]:
                    """Stop the web service."""
                    return FlextWebProtocols.Web.WebServiceProtocol.stop_service()

            class _WebRepositoryBase:
                """Base implementation of WebRepositoryProtocol for testing."""

                def find_by_criteria(
                    self,
                    criteria: t.WebCore.RequestDict,
                ) -> FlextResult[list[t.WebCore.ResponseDict]]:
                    """Find entities by criteria."""
                    return FlextWebProtocols.Web.WebRepositoryProtocol.find_by_criteria(
                        criteria
                    )

            class _WebHandlerBase:
                """Base implementation of WebHandlerProtocol for testing."""

                def handle_request(
                    self,
                    request: t.WebCore.RequestDict,
                ) -> FlextResult[t.WebCore.ResponseDict]:
                    """Handle web request and return response."""
                    return FlextWebProtocols.Web.WebHandlerProtocol.handle_request(
                        request
                    )

            class _WebConnectionBase:
                """Base implementation of WebConnectionProtocol for testing."""

                def get_endpoint_url(self) -> str:
                    """Get the web service endpoint URL."""
                    return (
                        FlextWebProtocols.Web.WebConnectionProtocol.get_endpoint_url()
                    )

            class _WebTemplateRendererBase:
                """Base implementation of WebTemplateRendererProtocol for testing."""

                def render_template(
                    self,
                    template_name: str,
                    context: t.WebCore.RequestDict,
                ) -> FlextResult[str]:
                    """Render template with context data."""
                    return FlextWebProtocols.Web.WebTemplateRendererProtocol.render_template(
                        template_name,
                        context,
                    )

                def render_dashboard(
                    self,
                    data: t.WebCore.ResponseDict,
                ) -> FlextResult[str]:
                    """Render dashboard template with data."""
                    return FlextWebProtocols.Web.WebTemplateRendererProtocol.render_dashboard(
                        data
                    )

            class _WebTemplateEngineBase:
                """Base implementation of WebTemplateEngineProtocol for testing."""

                def load_template_config(
                    self,
                    config: t.WebCore.RequestDict,
                ) -> FlextResult[bool]:
                    """Load template engine configuration."""
                    return FlextWebProtocols.Web.WebTemplateEngineProtocol.load_template_config(
                        config
                    )

                def get_template_config(
                    self,
                ) -> FlextResult[t.WebCore.ResponseDict]:
                    """Get current template engine configuration."""
                    return FlextWebProtocols.Web.WebTemplateEngineProtocol.get_template_config()

                def validate_template_config(
                    self,
                    config: t.WebCore.RequestDict,
                ) -> FlextResult[bool]:
                    """Validate template engine configuration."""
                    return FlextWebProtocols.Web.WebTemplateEngineProtocol.validate_template_config(
                        config,
                    )

                def render(
                    self,
                    template: str,
                    context: t.WebCore.RequestDict,
                ) -> FlextResult[str]:
                    """Render template string with context."""
                    return FlextWebProtocols.Web.WebTemplateEngineProtocol.render(
                        template, context
                    )

                def add_filter(
                    self, name: str, filter_func: Callable[[str], str]
                ) -> None:
                    """Add template filter function."""
                    FlextWebProtocols.Web.template_filters[name] = filter_func

                def add_global(
                    self,
                    name: str,
                    *,
                    value: t.GeneralValueType,
                ) -> None:
                    """Add template global variable."""
                    FlextWebProtocols.Web.template_globals[name] = (
                        dict(value) if isinstance(value, Mapping) else value
                    )

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
                    request_count_value = FlextWebProtocols.Web.web_metrics.get(
                        "requests", 0
                    )
                    request_count = (
                        request_count_value
                        if isinstance(request_count_value, int)
                        else 0
                    )
                    next_count = request_count + 1
                    FlextWebProtocols.Web.web_metrics["requests"] = next_count

                    avg_value = FlextWebProtocols.Web.web_metrics.get(
                        "avg_response_time_ms",
                        0,
                    )
                    previous_avg = avg_value if isinstance(avg_value, int) else 0
                    average_response_time_ms = (
                        (previous_avg * request_count) + (response_time * 1000)
                    ) / next_count
                    FlextWebProtocols.Web.web_metrics["avg_response_time_ms"] = int(
                        average_response_time_ms,
                    )

                    status_value = request.get("status")
                    if (
                        isinstance(status_value, str)
                        and status_value.lower() == c.Web.Status.ERROR.value
                    ):
                        error_count_value = FlextWebProtocols.Web.web_metrics.get(
                            "errors", 0
                        )
                        error_count = (
                            error_count_value
                            if isinstance(error_count_value, int)
                            else 0
                        )
                        FlextWebProtocols.Web.web_metrics["errors"] = error_count + 1

                def get_web_metrics(self) -> t.WebCore.ResponseDict:
                    """Get web application metrics."""
                    return FlextWebProtocols.Web.WebMonitoringProtocol.get_web_metrics()


p = FlextWebProtocols


def create_app(name: str, port: int, host: str) -> FlextResult[t.WebCore.ResponseDict]:
    """Create a new web application."""
    return FlextWebProtocols.Web.WebAppManagerProtocol.create_app(name, port, host)


def start_app(app_id: str) -> FlextResult[t.WebCore.ResponseDict]:
    """Start a web application."""
    return FlextWebProtocols.Web.WebAppManagerProtocol.start_app(app_id)


def stop_app(app_id: str) -> FlextResult[t.WebCore.ResponseDict]:
    """Stop a web application."""
    return FlextWebProtocols.Web.WebAppManagerProtocol.stop_app(app_id)


def list_apps() -> FlextResult[list[t.WebCore.ResponseDict]]:
    """List all web applications."""
    return FlextWebProtocols.Web.WebAppManagerProtocol.list_apps()


__all__ = [
    "FlextWebProtocols",
    "create_app",
    "list_apps",
    "p",
    "start_app",
    "stop_app",
]
