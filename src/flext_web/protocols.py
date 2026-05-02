"""FLEXT Web protocols + service helpers — extends ``p`` with web-specific contracts.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from collections.abc import (
    Awaitable,
    Callable,
    Sequence,
)
from copy import deepcopy
from threading import Thread
from time import sleep
from typing import ClassVar, Protocol, override, runtime_checkable
from uuid import uuid4
from wsgiref.simple_server import WSGIServer, make_server

import flask
import uvicorn
from fastapi import FastAPI
from flext_cli import p, r
from starlette.requests import Request as StarletteRequest
from starlette.responses import Response as StarletteResponse
from werkzeug.serving import BaseWSGIServer

from flext_web import c, e, m, t, u


class FlextWebProtocols(p):
    """Web-specific @runtime_checkable Protocol surface extending ``p``."""

    class Web:
        """Web domain-specific protocols."""

        @runtime_checkable
        class FastApiLikeApp(Protocol):
            """Duck-type protocol for FastAPI-like framework apps."""

            def add_api_route(
                self,
                path: str,
                endpoint: Callable[..., t.Web.ResponseDict],
                **kwargs: t.Scalar,
            ) -> None:
                """Register an API route."""
                ...

            def middleware(
                self,
                middleware_type: str,
            ) -> Callable[..., Callable[..., StarletteResponse]]:
                """Register middleware."""
                ...

        @runtime_checkable
        class FlaskLikeApp(Protocol):
            """Duck-type protocol for Flask-like framework apps."""

            def before_request(self, f: Callable[..., None]) -> Callable[..., None]:
                """Register a before-request hook."""
                ...

            def route(
                self,
                rule: str,
                **options: t.Scalar,
            ) -> Callable[..., Callable[..., t.Web.ResponseDict]]:
                """Register a URL route."""
                ...

        apps_registry: ClassVar[dict[str, t.Web.ResponseDict]] = {}
        framework_instances: ClassVar[dict[str, flask.Flask | FastAPI]] = {}
        app_runtimes: ClassVar[dict[str, m.Web.AppRuntimeInfo]] = {}
        service_state: ClassVar[dict[str, bool]] = {
            "routes_initialized": False,
            "middleware_configured": False,
            "service_running": False,
        }
        web_metrics: ClassVar[dict[str, int | str]] = {}
        template_config: ClassVar[t.Web.RequestDict] = {}
        template_globals: ClassVar[dict[str, t.JsonValue]] = {}
        template_filters: ClassVar[dict[str, Callable[[str], str]]] = {}

        @classmethod
        def _create_framework_app(
            cls,
            name: str,
        ) -> p.Result[tuple[flask.Flask | FastAPI, str, str]]:
            try:
                fastapi_app = FastAPI(
                    title=name,
                    version=c.Web.DEFAULT_VERSION_STRING,
                    description=c.Web.API_DEFAULT_DESCRIPTION,
                    docs_url=c.Web.API_DOCS_URL,
                    redoc_url=c.Web.API_REDOC_URL,
                    openapi_url=c.Web.API_OPENAPI_URL,
                )
            except c.EXC_OS_RUNTIME_TYPE as exc:
                fastapi_error = f"Failed to create FastAPI application: {exc}"
            else:
                return r[tuple[flask.Flask | FastAPI, str, str]].ok((
                    fastapi_app,
                    c.Web.FRAMEWORK_FASTAPI,
                    c.Web.FRAMEWORK_INTERFACE_ASGI,
                ))

            try:
                flask_app = flask.Flask(name)
                flask_app.config["SECRET_KEY"] = c.Web.DEFAULT_SECRET_KEY
                flask_app.config["DEBUG"] = c.Web.DEFAULT_DEBUG_MODE
                flask_app.config["TESTING"] = False
            except c.EXC_OS_RUNTIME_TYPE as exc:
                return r[tuple[flask.Flask | FastAPI, str, str]].fail(
                    f"{fastapi_error}; Failed to create Flask application: {exc}",
                )

            return r[tuple[flask.Flask | FastAPI, str, str]].ok((
                flask_app,
                c.Web.FRAMEWORK_FLASK,
                c.Web.FRAMEWORK_INTERFACE_WSGI,
            ))

        @staticmethod
        def _configure_framework_app_middleware(
            app_instance: flask.Flask | FastAPI,
        ) -> None:
            if isinstance(app_instance, FastAPI):

                async def fastapi_metrics_middleware(
                    request: StarletteRequest,
                    call_next: Callable[
                        [StarletteRequest],
                        Awaitable[StarletteResponse],
                    ],
                ) -> StarletteResponse:
                    response = await call_next(request)
                    FlextWebProtocols.Web.record_request_metric(
                        c.Web.RESPONSE_STATUS_SUCCESS, 0
                    )
                    return response

                app_instance.middleware("http")(fastapi_metrics_middleware)

            else:
                # app_instance is flask.Flask (from the if/elif chain above)
                def flask_metrics_middleware() -> None:
                    FlextWebProtocols.Web.record_request_metric(
                        c.Web.RESPONSE_STATUS_SUCCESS, 0
                    )

                app_instance.before_request(flask_metrics_middleware)

        @staticmethod
        def _configure_framework_app_routes(
            app_instance: flask.Flask | FastAPI,
            app_id: str,
        ) -> None:
            if isinstance(app_instance, FastAPI):

                def fastapi_health() -> t.Web.ResponseDict:
                    return {
                        "status": c.Web.RESPONSE_STATUS_HEALTHY,
                        "service": c.Web.SERVICE_NAME,
                        "app_id": app_id,
                    }

                app_instance.add_api_route(
                    "/protocol/health",
                    fastapi_health,
                    methods=["GET"],
                )
            else:
                # app_instance is flask.Flask (from the if/elif chain above)
                def flask_health() -> t.Web.ResponseDict:
                    return {
                        "status": c.Web.RESPONSE_STATUS_HEALTHY,
                        "service": c.Web.SERVICE_NAME_FLASK,
                        "app_id": app_id,
                    }

                app_instance.add_url_rule(
                    "/protocol/health",
                    "flask_health",
                    flask_health,
                )

        @staticmethod
        def _is_valid_port(port: int) -> bool:
            min_port, max_port = c.Web.VALIDATION_PORT_RANGE
            return min_port <= port <= max_port

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
                previous_avg * request_count + response_time_ms
            ) / next_count
            FlextWebProtocols.Web.web_metrics["avg_response_time_ms"] = int(
                average_response_time_ms,
            )
            if (
                isinstance(status, str)
                and status.lower() == c.Web.RESPONSE_STATUS_ERROR
            ):
                error_count_value = FlextWebProtocols.Web.web_metrics.get("errors", 0)
                error_count = (
                    error_count_value if isinstance(error_count_value, int) else 0
                )
                FlextWebProtocols.Web.web_metrics["errors"] = error_count + 1

        @staticmethod
        def _start_app_runtime(
            app_id: str,
            app_data: t.Web.ResponseDict,
            app_instance: flask.Flask | FastAPI,
        ) -> p.Result[m.Web.AppRuntimeInfo]:
            host = app_data.get("host")
            port = app_data.get("port")
            interface = app_data.get("interface")
            error_message = f"Unsupported app interface for runtime start: {interface}"
            runtime_info: m.Web.AppRuntimeInfo | None = None
            if not isinstance(host, str) or not isinstance(port, int):
                error_message = f"Invalid runtime configuration for app: {app_id}"
            elif interface == c.Web.FRAMEWORK_INTERFACE_ASGI:
                try:
                    settings = uvicorn.Config(
                        app=app_instance,
                        host=host,
                        port=port,
                        log_level="warning",
                        ws="none",
                    )
                    server = uvicorn.Server(settings)
                    thread = Thread(
                        target=server.run,
                        daemon=True,
                        name=f"flext-web-{app_id}",
                    )
                    thread.start()
                    sleep(0.05)
                    if thread.is_alive():
                        runtime_info = m.Web.AppRuntimeInfo(
                            runner=c.Web.FRAMEWORK_RUNNER_UVICORN,
                            server=server,
                            thread=thread,
                        )
                    else:
                        error_message = (
                            f"ASGI runtime exited immediately for app: {app_id}"
                        )
                except c.EXC_OS_RUNTIME_TYPE as exc:
                    error_message = (
                        f"Failed to start ASGI runtime for app {app_id}: {exc}"
                    )
            elif interface == c.Web.FRAMEWORK_INTERFACE_WSGI and isinstance(
                app_instance,
                flask.Flask,
            ):
                try:
                    wsgi_server: WSGIServer = make_server(host, port, app_instance)
                    thread = Thread(
                        target=wsgi_server.serve_forever,
                        daemon=True,
                        name=f"flext-web-{app_id}",
                    )
                    thread.start()
                    sleep(0.05)
                    if thread.is_alive():
                        runtime_info = m.Web.AppRuntimeInfo(
                            runner=c.Web.FRAMEWORK_RUNNER_WERKZEUG,
                            server=wsgi_server,
                            thread=thread,
                        )
                    else:
                        error_message = (
                            f"WSGI runtime exited immediately for app: {app_id}"
                        )
                except (
                    RuntimeError,
                    OSError,
                    ValueError,
                    TypeError,
                    AttributeError,
                ) as exc:
                    error_message = (
                        f"Failed to start WSGI runtime for app {app_id}: {exc}"
                    )
            return (
                r[m.Web.AppRuntimeInfo].ok(runtime_info)
                if runtime_info is not None
                else r[m.Web.AppRuntimeInfo].fail(error_message)
            )

        @staticmethod
        def _stop_app_runtime(
            app_id: str,
            runtime: m.Web.AppRuntimeInfo,
        ) -> p.Result[bool]:
            runner: str = runtime.runner
            server: uvicorn.Server | WSGIServer = runtime.server
            thread: Thread = runtime.thread
            try:
                if runner == c.Web.FRAMEWORK_RUNNER_UVICORN:
                    if not isinstance(server, uvicorn.Server):
                        return r[bool].fail(
                            f"Missing ASGI server instance for app: {app_id}",
                        )
                    server.should_exit = True
                elif runner == c.Web.FRAMEWORK_RUNNER_WERKZEUG:
                    if not isinstance(server, BaseWSGIServer):
                        return r[bool].fail(
                            f"Missing WSGI server instance for app: {app_id}",
                        )
                    server.shutdown()
                    server.server_close()
                else:
                    return r[bool].fail(f"Unsupported runtime runner for app: {app_id}")
                thread.join(timeout=2.0)
                if thread.is_alive():
                    return r[bool].fail(
                        f"Runtime thread did not stop cleanly for app: {app_id}",
                    )
            except (RuntimeError, AttributeError, OSError) as exc:
                return r[bool].fail(f"Failed to stop app runtime {app_id}: {exc}")
            return r[bool].ok(True)

        record_request_metric: ClassVar[Callable[..., None]] = _record_request_metric
        create_framework_app: ClassVar[
            Callable[..., p.Result[tuple[flask.Flask | FastAPI, str, str]]]
        ] = _create_framework_app
        configure_framework_app_routes: ClassVar[Callable[..., None]] = (
            _configure_framework_app_routes
        )
        configure_framework_app_middleware: ClassVar[Callable[..., None]] = (
            _configure_framework_app_middleware
        )
        start_app_runtime: ClassVar[Callable[..., p.Result[m.Web.AppRuntimeInfo]]] = (
            _start_app_runtime
        )
        stop_app_runtime: ClassVar[Callable[..., p.Result[bool]]] = _stop_app_runtime
        is_valid_port: ClassVar[Callable[[int], bool]] = _is_valid_port

        @runtime_checkable
        class WebAppManager(p.Service[t.Web.ResponseDict], Protocol):
            """Protocol for web application lifecycle management."""

            @staticmethod
            def create_app(
                name: str,
                port: int,
                host: str,
            ) -> p.Result[t.Web.ResponseDict]:
                """Create a new web application."""
                normalized_name = name.strip()
                normalized_host = host.strip()
                if len(normalized_name) < c.Web.SERVER_MIN_APP_NAME_LENGTH:
                    return r[t.Web.ResponseDict].fail(
                        f"Application name must be at least {c.Web.SERVER_MIN_APP_NAME_LENGTH} characters",
                    )
                if normalized_name.isdigit():
                    return r[t.Web.ResponseDict].fail(
                        "Application name cannot be numeric-only",
                    )
                if not normalized_host:
                    return r[t.Web.ResponseDict].fail("Host cannot be empty")
                if not FlextWebProtocols.Web.is_valid_port(port):
                    min_port, max_port = c.Web.VALIDATION_PORT_RANGE
                    return r[t.Web.ResponseDict].fail(
                        f"Port must be between {min_port} and {max_port}",
                    )
                framework_result = FlextWebProtocols.Web.create_framework_app(
                    normalized_name,
                )
                if framework_result.failure:
                    return r[t.Web.ResponseDict].fail(framework_result.error)
                app_instance, framework_name, interface_type = framework_result.value
                app_id = str(uuid4())
                FlextWebProtocols.Web.configure_framework_app_routes(
                    app_instance,
                    app_id,
                )
                FlextWebProtocols.Web.configure_framework_app_middleware(app_instance)
                app_data: t.Web.ResponseDict = {
                    "id": app_id,
                    "name": normalized_name,
                    "port": port,
                    "host": normalized_host,
                    "status": c.Web.Status.STOPPED.value,
                    "created_at": u.generate_iso_timestamp(),
                    "framework": framework_name,
                    "interface": interface_type,
                }
                FlextWebProtocols.Web.apps_registry[app_id] = app_data
                FlextWebProtocols.Web.framework_instances[app_id] = app_instance
                return r[t.Web.ResponseDict].ok(app_data)

            @staticmethod
            def list_apps() -> p.Result[Sequence[t.Web.ResponseDict]]:
                """List all web applications."""
                apps = [
                    deepcopy(app)
                    for app in FlextWebProtocols.Web.apps_registry.values()
                ]
                return r[Sequence[t.Web.ResponseDict]].ok(apps)

            @staticmethod
            def start_app(app_id: str) -> p.Result[t.Web.ResponseDict]:
                """Start a web application."""
                app_data = FlextWebProtocols.Web.apps_registry.get(app_id)
                if app_data is None:
                    return e.fail_not_found(
                        "Application", app_id, result_type=r[t.Web.ResponseDict]
                    )
                if app_data.get("status") == c.Web.Status.RUNNING.value:
                    return r[t.Web.ResponseDict].fail(
                        f"Application already running: {app_id}",
                    )
                app_instance = FlextWebProtocols.Web.framework_instances.get(app_id)
                if app_instance is None:
                    return e.fail_not_found(
                        "Application runtime instance",
                        app_id,
                        result_type=r[t.Web.ResponseDict],
                    )
                runtime_result = FlextWebProtocols.Web.start_app_runtime(
                    app_id,
                    app_data,
                    app_instance,
                )
                if runtime_result.failure:
                    return r[t.Web.ResponseDict].fail(runtime_result.error)
                updated_app = deepcopy(app_data)
                updated_app["status"] = c.Web.Status.RUNNING.value
                FlextWebProtocols.Web.apps_registry[app_id] = updated_app
                FlextWebProtocols.Web.app_runtimes[app_id] = runtime_result.value
                return r[t.Web.ResponseDict].ok(updated_app)

            @staticmethod
            def stop_app(app_id: str) -> p.Result[t.Web.ResponseDict]:
                """Stop a running web application."""
                app_data = FlextWebProtocols.Web.apps_registry.get(app_id)
                if app_data is None:
                    return e.fail_not_found(
                        "Application", app_id, result_type=r[t.Web.ResponseDict]
                    )
                if app_data.get("status") != c.Web.Status.RUNNING.value:
                    return r[t.Web.ResponseDict].fail(
                        f"Application not running: {app_id}",
                    )
                runtime = FlextWebProtocols.Web.app_runtimes.get(app_id)
                if runtime is None:
                    return r[t.Web.ResponseDict].fail(
                        f"Application runtime not found for stop: {app_id}",
                    )
                stop_runtime_result = FlextWebProtocols.Web.stop_app_runtime(
                    app_id,
                    runtime,
                )
                if stop_runtime_result.failure:
                    return r[t.Web.ResponseDict].fail(stop_runtime_result.error)
                updated_app = deepcopy(app_data)
                updated_app["status"] = c.Web.Status.STOPPED.value
                FlextWebProtocols.Web.apps_registry[app_id] = updated_app
                _ = FlextWebProtocols.Web.app_runtimes.pop(app_id, None)
                return r[t.Web.ResponseDict].ok(updated_app)

        @runtime_checkable
        class WebResponseFormatter(
            p.Service[t.Web.ResponseDict],
            Protocol,
        ):
            """Protocol for web response formatting."""

            @staticmethod
            def create_json_response(
                data: t.Web.ResponseDict,
            ) -> t.Web.ResponseDict:
                """Create a JSON response."""
                response: t.Web.ResponseDict = {
                    c.Web.HTTP_HEADER_CONTENT_TYPE: c.Web.HTTP_CONTENT_TYPE_JSON,
                }
                response.update(deepcopy(data))
                return response

            @staticmethod
            def format_error(error: Exception) -> t.Web.ResponseDict:
                """Format error response data."""
                result: t.Web.ResponseDict = {
                    "status": c.Web.RESPONSE_STATUS_ERROR,
                    "message": str(error),
                }
                return result

            @staticmethod
            def format_success(data: t.Web.ResponseDict) -> t.Web.ResponseDict:
                """Format successful response data."""
                response: t.Web.ResponseDict = {
                    "status": c.Web.RESPONSE_STATUS_SUCCESS,
                }
                response.update(deepcopy(data))
                return response

        @runtime_checkable
        class WebFrameworkInterface(
            p.Service[t.Web.ResponseDict],
            Protocol,
        ):
            """Protocol for web framework integration."""

            @staticmethod
            def create_json_response(
                data: t.Web.ResponseDict,
            ) -> t.Web.ResponseDict:
                """Create a JSON response."""
                response: t.Web.ResponseDict = {
                    c.Web.HTTP_HEADER_CONTENT_TYPE: c.Web.HTTP_CONTENT_TYPE_JSON,
                }
                response.update(deepcopy(data))
                return response

            @staticmethod
            def json_request(_request: t.Web.RequestDict) -> bool:
                """Check if request contains JSON data."""
                content_type = _request.get(c.Web.HTTP_HEADER_CONTENT_TYPE)
                if isinstance(content_type, str):
                    return c.Web.HTTP_CONTENT_TYPE_JSON in content_type.lower()
                headers = _request.get("headers")
                if isinstance(headers, dict):
                    nested_content_type = headers.get(c.Web.HTTP_HEADER_CONTENT_TYPE)
                    if isinstance(nested_content_type, str):
                        return (
                            c.Web.HTTP_CONTENT_TYPE_JSON in nested_content_type.lower()
                        )
                return False

        @runtime_checkable
        class WebService(p.Service[t.Web.ResponseDict], Protocol):
            """Base web service protocol."""

            @staticmethod
            def configure_middleware() -> p.Result[bool]:
                """Configure web service middleware."""
                FlextWebProtocols.Web.service_state["middleware_configured"] = True
                return r[bool].ok(value=True)

            @staticmethod
            def initialize_routes() -> p.Result[bool]:
                """Initialize web service routes."""
                FlextWebProtocols.Web.service_state["routes_initialized"] = True
                return r[bool].ok(value=True)

            @staticmethod
            def start_service() -> p.Result[bool]:
                """Start the web service."""
                state = FlextWebProtocols.Web.service_state
                if not state["routes_initialized"]:
                    return r[bool].fail(
                        "Routes must be initialized before starting service",
                    )
                if not state["middleware_configured"]:
                    return r[bool].fail(
                        "Middleware must be configured before starting service",
                    )
                if state["service_running"]:
                    return r[bool].fail("Service is already running")
                state["service_running"] = True
                return r[bool].ok(value=True)

            @staticmethod
            def stop_service() -> p.Result[bool]:
                """Stop the web service."""
                state = FlextWebProtocols.Web.service_state
                if not state["service_running"]:
                    return r[bool].fail("Service is not running")
                state["service_running"] = False
                return r[bool].ok(value=True)

        @runtime_checkable
        class WebRepository(Protocol):
            """Base web repository protocol for data access."""

            @staticmethod
            def fetch_by_id(entity_id: str) -> p.Result[t.Web.ResponseDict]:
                """Return a single app by ID or failure when not found."""
                app_data = FlextWebProtocols.Web.apps_registry.get(entity_id)
                if app_data is None:
                    return e.fail_not_found(
                        "Application", entity_id, result_type=r[t.Web.ResponseDict]
                    )
                return r[t.Web.ResponseDict].ok(deepcopy(app_data))

            @staticmethod
            def save(entity: t.Web.ResponseDict) -> p.Result[t.Web.ResponseDict]:
                """Persist an app entity and return a defensive copy."""
                entity_id = entity.get("id")
                if not isinstance(entity_id, str):
                    return r[t.Web.ResponseDict].fail("Entity id(str) is required")
                FlextWebProtocols.Web.apps_registry[entity_id] = deepcopy(entity)
                return r[t.Web.ResponseDict].ok(deepcopy(entity))

            @staticmethod
            def delete(entity_id: str) -> p.Result[bool]:
                """Delete an app entity by ID."""
                removed = FlextWebProtocols.Web.apps_registry.pop(entity_id, None)
                if removed is None:
                    return e.fail_not_found(
                        "Application", entity_id, result_type=r[bool]
                    )
                return r[bool].ok(True)

            @staticmethod
            def find_all() -> p.Result[Sequence[t.Web.ResponseDict]]:
                """Return all registered app entities as defensive copies."""
                return r[Sequence[t.Web.ResponseDict]].ok([
                    deepcopy(app)
                    for app in FlextWebProtocols.Web.apps_registry.values()
                ])

            @staticmethod
            def find_by_criteria(
                criteria: t.Web.RequestDict,
            ) -> p.Result[Sequence[t.Web.ResponseDict]]:
                """Find entities by criteria."""
                matches: t.SequenceOf[t.Web.ResponseDict] = [
                    deepcopy(app_data)
                    for app_data in FlextWebProtocols.Web.apps_registry.values()
                    if all(
                        app_data.get(key) == expected_value
                        for key, expected_value in criteria.items()
                    )
                ]
                return r[Sequence[t.Web.ResponseDict]].ok(matches)

        @runtime_checkable
        class WebHandler(Protocol):
            """Web handler protocol for request/response patterns."""

            @staticmethod
            def handle_request(
                request: t.Web.RequestDict,
            ) -> p.Result[t.Web.ResponseDict]:
                """Handle web request and return response."""
                action = request.get("action")
                if action == c.Web.ACTION_CREATE:
                    name = request.get("name")
                    port = request.get("port")
                    host = request.get("host")
                    if (
                        not isinstance(name, str)
                        or not isinstance(port, int)
                        or (not isinstance(host, str))
                    ):
                        return r[t.Web.ResponseDict].fail(
                            "create action requires name(str), port(int), host(str)",
                        )
                    return FlextWebProtocols.Web.WebAppManager.create_app(
                        name=name,
                        port=port,
                        host=host,
                    )
                if action == c.Web.ACTION_START:
                    app_id = request.get("app_id")
                    if not isinstance(app_id, str):
                        return r[t.Web.ResponseDict].fail(
                            "start action requires app_id(str)",
                        )
                    return FlextWebProtocols.Web.WebAppManager.start_app(app_id)
                if action == c.Web.ACTION_STOP:
                    app_id = request.get("app_id")
                    if not isinstance(app_id, str):
                        return r[t.Web.ResponseDict].fail(
                            "stop action requires app_id(str)",
                        )
                    return FlextWebProtocols.Web.WebAppManager.stop_app(app_id)
                if action == c.Web.ACTION_LIST:
                    return FlextWebProtocols.Web.WebAppManager.list_apps().map(
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
                return r[t.Web.ResponseDict].ok(deepcopy(request))

            def execute(
                self,
                command: t.Web.RequestDict,
            ) -> p.Result[t.Web.ResponseDict]:
                """Execute command (extends p.Handler pattern)."""
                return FlextWebProtocols.Web.WebHandler.handle_request(command)

        @runtime_checkable
        class WebConnection(p.Service[t.Web.ResponseDict], Protocol):
            """Web connection protocol for external systems."""

            @staticmethod
            def endpoint_url() -> str:
                """Get the web service endpoint URL."""
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
        class WebLogger(p.Service[t.Web.ResponseDict], Protocol):
            """Web logging protocol."""

            @staticmethod
            def _merged_status(
                main: t.Web.RequestDict | t.Web.ResponseDict,
                context: t.Web.RequestDict | t.Web.ResponseDict | None,
            ) -> str | None:
                """Extract status from main dict, allowing context override."""
                merged: str | None = None
                if isinstance(context, dict):
                    cs = context.get("status")
                    if isinstance(cs, str):
                        merged = cs
                ms = main.get("status")
                if isinstance(ms, str):
                    merged = ms
                return merged

            def log_request(
                self,
                request: t.Web.RequestDict,
                context: t.Web.RequestDict | None = None,
            ) -> None:
                """Log web request with context."""
                FlextWebProtocols.Web.record_request_metric(
                    self._merged_status(request, context), 0
                )

            def log_response(
                self,
                response: t.Web.ResponseDict,
                context: t.Web.ResponseDict | None = None,
            ) -> None:
                """Log web response with context."""
                FlextWebProtocols.Web.record_request_metric(
                    self._merged_status(response, context), 0
                )

        @runtime_checkable
        class WebTemplateRenderer(
            p.Service[t.Web.ResponseDict],
            Protocol,
        ):
            """Protocol for web template rendering."""

            @staticmethod
            def render_dashboard(data: t.Web.ResponseDict) -> p.Result[str]:
                """Render dashboard template with data."""
                app_name = data.get("service", c.Web.SERVICE_NAME)
                status = data.get("status", c.Web.Status.STOPPED.value)
                html = f"<html><body><h1>{app_name}</h1><p>Status: {status}</p></body></html>"
                return r[str].ok(html)

            @staticmethod
            def render_template(
                template_name: str,
                context: t.Web.RequestDict,
            ) -> p.Result[str]:
                """Render template with context data."""
                rendered = template_name
                for key, value in context.items():
                    if isinstance(value, (str, int, bool)):
                        rendered = rendered.replace(f"{{{{{key}}}}}", str(value))
                return r[str].ok(rendered)

        @runtime_checkable
        class WebTemplateEngine(
            p.Service[t.Web.ResponseDict],
            Protocol,
        ):
            """Protocol for web template engine operations."""

            @staticmethod
            def template_config() -> p.Result[t.Web.ResponseDict]:
                """Return current template engine configuration."""
                return r[t.Web.ResponseDict].ok(
                    deepcopy(FlextWebProtocols.Web.template_config),
                )

            @staticmethod
            def load_template_config(
                settings: t.Web.RequestDict,
            ) -> p.Result[bool]:
                """Load template engine configuration."""
                FlextWebProtocols.Web.template_config = deepcopy(settings)
                return r[bool].ok(value=True)

            @staticmethod
            def render(template: str, context: t.Web.RequestDict) -> p.Result[str]:
                """Render template string with context."""
                full_context = deepcopy(FlextWebProtocols.Web.template_globals)
                for context_key, context_value in context.items():
                    full_context[context_key] = (
                        context_value
                        if u.primitive(context_value)
                        else str(context_value)
                    )
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
                return r[str].ok(rendered)

            @staticmethod
            def validate_template_config(
                settings: t.Web.RequestDict,
            ) -> p.Result[bool]:
                """Validate template engine configuration."""
                allowed_keys = {"template_dir", "autoescape", "cache_enabled"}
                invalid_keys = [key for key in settings if key not in allowed_keys]
                if invalid_keys:
                    return r[bool].fail(
                        f"Invalid template settings keys: {', '.join(invalid_keys)}",
                    )
                return r[bool].ok(value=True)

            def add_filter(self, name: str, filter_func: Callable[[str], str]) -> None:
                """Add template filter function."""
                FlextWebProtocols.Web.template_filters[name] = filter_func

            def add_global(self, name: str, *, value: t.JsonValue) -> None:
                """Add template global variable."""
                FlextWebProtocols.Web.template_globals[name] = value

        @runtime_checkable
        class WebMonitoring(p.Service[t.Web.ResponseDict], Protocol):
            """Web monitoring protocol for observability."""

            @staticmethod
            def web_health_status() -> t.Web.ResponseDict:
                """Get web application health status."""
                service_running = FlextWebProtocols.Web.service_state["service_running"]
                return {
                    "status": c.Web.RESPONSE_STATUS_HEALTHY
                    if service_running
                    else c.Web.Status.STOPPED.value,
                    "service": c.Web.SERVICE_NAME,
                    "routes_initialized": FlextWebProtocols.Web.service_state[
                        "routes_initialized"
                    ],
                    "middleware_configured": FlextWebProtocols.Web.service_state[
                        "middleware_configured"
                    ],
                }

            @staticmethod
            def web_metrics() -> t.Web.ResponseDict:
                """Get web application metrics."""
                metrics: t.Web.ResponseDict = {}
                for key, val in FlextWebProtocols.Web.web_metrics.items():
                    metrics[key] = u.to_int(val) if isinstance(val, float) else val
                return metrics

            def record_web_request(
                self,
                request: t.Web.RequestDict,
                response_time: float,
            ) -> None:
                """Record web request metrics."""
                status_value = request.get("status")
                status = status_value if isinstance(status_value, str) else None
                response_time_ms = int(max(response_time, 0) * 1000)
                FlextWebProtocols.Web.record_request_metric(status, response_time_ms)

        @runtime_checkable
        class ConfigValue(Protocol):
            """Protocol for configuration values."""

            value: t.Scalar

            @override
            def __str__(self) -> str:
                """Convert to string."""
                return str(self.value)

            def __bool__(self) -> bool:
                """Convert to boolean."""
                return bool(self.value)

            def __int__(self) -> int:
                """Convert to integer."""
                if isinstance(self.value, bool):
                    return int(self.value)
                if isinstance(self.value, int):
                    return self.value
                if isinstance(self.value, float):
                    return int(self.value)
                if isinstance(self.value, str):
                    try:
                        return int(self.value)
                    except ValueError:
                        return 0
                return 0  # datetime case

        @runtime_checkable
        class ResponseData(Protocol):
            """Protocol for response data structures."""

            def get(
                self,
                key: str,
                default: str | None = None,
            ) -> t.Scalar | t.StrSequence | None:
                """Get value by key with optional default."""
                ...

        class TestBases:
            """Namespace for test base implementations."""

            _flext_enforcement_exempt: ClassVar[bool] = True

            class _WebTemplateEngineBase:
                """Base implementation of WebTemplateEngine for testing."""

                def add_filter(
                    self,
                    name: str,
                    filter_func: Callable[[str], str],
                ) -> None:
                    """Add template filter function."""
                    FlextWebProtocols.Web.template_filters[name] = filter_func

                def add_global(self, name: str, *, value: t.JsonValue) -> None:
                    """Add template global variable."""
                    FlextWebProtocols.Web.template_globals[name] = value

                def template_config(self) -> p.Result[t.Web.ResponseDict]:
                    """Return current template engine configuration."""
                    return FlextWebProtocols.Web.WebTemplateEngine.template_config()

                def load_template_config(
                    self,
                    settings: t.Web.RequestDict,
                ) -> p.Result[bool]:
                    """Load template engine configuration."""
                    return FlextWebProtocols.Web.WebTemplateEngine.load_template_config(
                        settings,
                    )

                def render(
                    self,
                    template: str,
                    context: t.Web.RequestDict,
                ) -> p.Result[str]:
                    """Render template string with context."""
                    return FlextWebProtocols.Web.WebTemplateEngine.render(
                        template,
                        context,
                    )

                def validate_template_config(
                    self,
                    settings: t.Web.RequestDict,
                ) -> p.Result[bool]:
                    """Validate template engine configuration."""
                    return FlextWebProtocols.Web.WebTemplateEngine.validate_template_config(
                        settings,
                    )

            class _WebMonitoringBase:
                """Base implementation of WebMonitoring for testing."""

                def web_health_status(self) -> t.Web.ResponseDict:
                    """Get web application health status."""
                    return FlextWebProtocols.Web.WebMonitoring.web_health_status()

                def web_metrics(self) -> t.Web.ResponseDict:
                    """Get web application metrics."""
                    return FlextWebProtocols.Web.WebMonitoring.web_metrics()

                def record_web_request(
                    self,
                    request: t.Web.RequestDict,
                    response_time: float,
                ) -> None:
                    """Record web request metrics."""
                    request_count_value = FlextWebProtocols.Web.web_metrics.get(
                        "requests",
                        0,
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
                        previous_avg * request_count + response_time * 1000
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
                            "errors",
                            0,
                        )
                        error_count = (
                            error_count_value
                            if isinstance(error_count_value, int)
                            else 0
                        )
                        FlextWebProtocols.Web.web_metrics["errors"] = error_count + 1


p = FlextWebProtocols

__all__: list[str] = ["FlextWebProtocols", "p"]
