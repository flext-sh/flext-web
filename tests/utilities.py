"""Test utilities for flext-web.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

import socket
import time
from collections.abc import Callable, Sequence
from threading import Lock
from typing import ClassVar

import pytest
from flext_tests import FlextTestsUtilities
from pydantic import BaseModel, ValidationError

from flext_core import r
from flext_web import FlextWebUtilities
from tests import c, m, p, t


class TestsFlextWebUtilities(FlextTestsUtilities, FlextWebUtilities):
    """Test utilities for flext-web."""

    class Web(FlextWebUtilities.Web):
        """Web domain test utilities."""

        class Tests:
            """Test-specific utilities."""

            @staticmethod
            def _is_numeric(value: t.RecursiveContainer | None) -> bool:
                """Return whether value is a numeric scalar excluding bool."""
                return isinstance(value, t.NUMERIC_TYPES) and not isinstance(
                    value,
                    bool,
                )

            @staticmethod
            def _to_float(
                value: t.RecursiveContainer | None, *, default: float
            ) -> float:
                """Normalize supported numeric values to float with fallback."""
                if isinstance(value, t.NUMERIC_TYPES) and not isinstance(value, bool):
                    return float(value)
                return default

            @staticmethod
            def _to_optional_float(value: t.RecursiveContainer | None) -> float | None:
                """Normalize supported numeric values to float or None."""
                if isinstance(value, t.NUMERIC_TYPES) and not isinstance(value, bool):
                    return float(value)
                return None

            class TestPortManager:
                """Thread-safe port allocation manager for test services."""

                _lock: ClassVar[Lock] = Lock()
                _allocated_ports: ClassVar[set[int]] = set()
                _current_port: ClassVar[int] = c.Web.Tests.TestPort.PORT_START

                @classmethod
                def allocate_port(cls) -> int:
                    """Allocate a unique port for testing."""
                    with cls._lock:
                        while cls._current_port in cls._allocated_ports:
                            cls._current_port += 1
                            if cls._current_port > c.Web.Tests.TestPort.PORT_END:
                                cls._current_port = c.Web.Tests.TestPort.PORT_START
                        port = cls._current_port
                        cls._allocated_ports.add(port)
                        cls._current_port += 1
                        return port

                @classmethod
                def release_port(cls, port: int) -> None:
                    """Release a previously allocated port."""
                    with cls._lock:
                        cls._allocated_ports.discard(port)

                @classmethod
                def reset(cls) -> None:
                    """Reset the allocated test ports."""
                    with cls._lock:
                        cls._allocated_ports.clear()
                        cls._current_port = c.Web.Tests.TestPort.PORT_START

            @staticmethod
            def wait_for_port(host: str, port: int, timeout: float = 5.0) -> bool:
                """Wait until a TCP port becomes reachable."""
                start_time = time.time()
                while time.time() - start_time < timeout:
                    try:
                        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
                            sock.settimeout(0.1)
                            if sock.connect_ex((host, port)) == 0:
                                return True
                    except OSError:
                        pass
                    time.sleep(0.1)
                return False

            @staticmethod
            def _wrap_result[T](result: p.Result[T]) -> p.Result[BaseModel]:
                """Wrap a typed result into `r[BaseModel]` for generic helpers."""
                if result.success:
                    value = result.value
                    if isinstance(value, BaseModel):
                        return r[BaseModel].ok(value)
                    return r[BaseModel].fail("Result value is not a BaseModel")
                return r[BaseModel].fail(result.error or "Unknown error")

            @staticmethod
            def assert_success[T](
                result: p.Result[T],
                message: str = "Operation should succeed",
            ) -> None:
                """Assert that a result succeeded."""
                if not result.success:
                    raise AssertionError(f"{message}: {result.error}")

            @staticmethod
            def assert_failure[T](
                result: p.Result[T],
                message: str = "Operation should fail",
            ) -> None:
                """Assert that a result failed."""
                if result.success:
                    raise AssertionError(message)

            @staticmethod
            def assert_result[T](
                result: p.Result[T],
                *,
                expected_success: bool = True,
            ) -> None:
                """Assert result state according to expectation."""
                if expected_success:
                    TestsFlextWebUtilities.Web.Tests.assert_success(result)
                else:
                    TestsFlextWebUtilities.Web.Tests.assert_failure(result)

            @staticmethod
            def create_entry(
                entry_type: str,
                **kwargs: t.RecursiveContainer,
            ) -> p.Result[BaseModel]:
                """Create test entities through runtime namespaced MRO factories."""
                if entry_type == "web_app":
                    name = kwargs.get("name")
                    host = kwargs.get("host")
                    port = kwargs.get("port")
                    if (
                        not isinstance(name, str)
                        or not isinstance(host, str)
                        or not isinstance(port, int)
                    ):
                        return r[BaseModel].fail("Invalid parameters for web_app")
                    try:
                        return TestsFlextWebUtilities.Web.Tests._wrap_result(
                            m.Web.create_web_app(
                                name=name,
                                host=host,
                                port=port,
                            ),
                        )
                    except (ValidationError, ValueError, TypeError) as exc:
                        return r[BaseModel].fail(str(exc))
                if entry_type == "http_request":
                    url = kwargs.get("url")
                    method = kwargs.get("method")
                    headers = kwargs.get("headers")
                    body = kwargs.get("body")
                    timeout = kwargs.get("timeout")
                    if not isinstance(url, str) or not isinstance(method, str):
                        return r[BaseModel].fail(
                            "Invalid parameters for http_request",
                        )
                    if headers is not None and not isinstance(headers, dict):
                        return r[BaseModel].fail("Invalid headers for http_request")
                    if body is not None and not isinstance(body, (str, dict)):
                        return r[BaseModel].fail("Invalid body for http_request")
                    if not TestsFlextWebUtilities.Web.Tests._is_numeric(timeout):
                        return r[BaseModel].fail("Invalid timeout for http_request")
                    narrow_headers: t.StrMapping | None = (
                        {k: str(v) for k, v in headers.items()}
                        if isinstance(headers, dict)
                        else None
                    )
                    narrow_body: str | t.ScalarMapping | None = (
                        body
                        if isinstance(body, str) or body is None
                        else {k: v for k, v in body.items() if u.primitive(v)}
                    )
                    return TestsFlextWebUtilities.Web.Tests._wrap_result(
                        t.create_http_request(
                            url=url,
                            method=method,
                            headers=narrow_headers,
                            body=narrow_body,
                            timeout=TestsFlextWebUtilities.Web.Tests._to_float(
                                timeout,
                                default=30.0,
                            ),
                        ),
                    )
                if entry_type == "http_response":
                    status_code = kwargs.get("status_code")
                    headers = kwargs.get("headers")
                    body = kwargs.get("body")
                    elapsed_time = kwargs.get("elapsed_time")
                    if not isinstance(status_code, int):
                        return r[BaseModel].fail(
                            "Invalid status_code for http_response",
                        )
                    if headers is not None and not isinstance(headers, dict):
                        return r[BaseModel].fail("Invalid headers for http_response")
                    if body is not None and not isinstance(body, (str, dict)):
                        return r[BaseModel].fail("Invalid body for http_response")
                    if elapsed_time is not None and not (
                        TestsFlextWebUtilities.Web.Tests._is_numeric(elapsed_time)
                    ):
                        return r[BaseModel].fail(
                            "Invalid elapsed_time for http_response",
                        )
                    resp_headers: t.StrMapping | None = (
                        {k: str(v) for k, v in headers.items()}
                        if isinstance(headers, dict)
                        else None
                    )
                    resp_body: str | t.ScalarMapping | None = (
                        body
                        if isinstance(body, str) or body is None
                        else {k: v for k, v in body.items() if u.primitive(v)}
                    )
                    return TestsFlextWebUtilities.Web.Tests._wrap_result(
                        t.create_http_response(
                            status_code=status_code,
                            headers=resp_headers,
                            body=resp_body,
                            elapsed_time=TestsFlextWebUtilities.Web.Tests._to_optional_float(
                                elapsed_time,
                            ),
                        ),
                    )
                if entry_type == "web_request":
                    url = kwargs.get("url")
                    method = kwargs.get("method")
                    headers = kwargs.get("headers")
                    body = kwargs.get("body")
                    timeout = kwargs.get("timeout")
                    query_params = kwargs.get("query_params")
                    client_ip = kwargs.get("client_ip")
                    user_agent = kwargs.get("user_agent")
                    if not isinstance(url, str) or not isinstance(method, str):
                        return r[BaseModel].fail("Invalid parameters for web_request")
                    try:
                        headers_dict: t.StrMapping = (
                            {}
                            if not isinstance(headers, dict)
                            else {k: str(v) for k, v in headers.items()}
                        )
                        body_value: t.ScalarMapping | str | None = (
                            body
                            if isinstance(body, str) or body is None
                            else (
                                {k: v for k, v in body.items() if u.primitive(v)}
                                if isinstance(body, dict)
                                else None
                            )
                        )
                        query_params_dict: t.ScalarMapping = (
                            {}
                            if not isinstance(query_params, dict)
                            else {
                                k: v for k, v in query_params.items() if u.primitive(v)
                            }
                        )
                        settings = t.Web.RequestConfig(
                            url=url,
                            method=method,
                            headers=headers_dict,
                            body=body_value,
                            timeout=TestsFlextWebUtilities.Web.Tests._to_float(
                                timeout,
                                default=30.0,
                            ),
                            query_params=query_params_dict,
                            client_ip=(
                                client_ip if isinstance(client_ip, str) else "127.0.0.1"
                            ),
                            user_agent=(
                                user_agent
                                if isinstance(user_agent, str)
                                else "test-client"
                            ),
                        )
                        return TestsFlextWebUtilities.Web.Tests._wrap_result(
                            t.create_web_request(settings),
                        )
                    except (ValidationError, ValueError, TypeError) as exc:
                        return r[BaseModel].fail(str(exc))
                if entry_type == "web_response":
                    status_code = kwargs.get("status_code")
                    request_id = kwargs.get("request_id")
                    headers = kwargs.get("headers")
                    body = kwargs.get("body")
                    elapsed_time = kwargs.get("elapsed_time")
                    content_type = kwargs.get("content_type")
                    content_length = kwargs.get("content_length")
                    processing_time_ms = kwargs.get("processing_time_ms")
                    if not isinstance(status_code, int):
                        return r[BaseModel].fail(
                            "Invalid status_code for web_response",
                        )
                    try:
                        headers_dict: t.StrMapping = (
                            {}
                            if not isinstance(headers, dict)
                            else {k: str(v) for k, v in headers.items()}
                        )
                        body_value: t.ScalarMapping | str | None = (
                            body
                            if isinstance(body, str) or body is None
                            else (
                                {k: v for k, v in body.items() if u.primitive(v)}
                                if isinstance(body, dict)
                                else None
                            )
                        )
                        settings = t.Web.ResponseConfig(
                            status_code=status_code,
                            request_id=(
                                request_id
                                if isinstance(request_id, str)
                                else "test-request"
                            ),
                            headers=headers_dict,
                            body=body_value,
                            elapsed_time=TestsFlextWebUtilities.Web.Tests._to_float(
                                elapsed_time,
                                default=0.0,
                            ),
                            content_type=(
                                content_type
                                if isinstance(content_type, str)
                                else "application/json"
                            ),
                            content_length=(
                                content_length if isinstance(content_length, int) else 0
                            ),
                            processing_time_ms=TestsFlextWebUtilities.Web.Tests._to_float(
                                processing_time_ms,
                                default=0.0,
                            ),
                        )
                        return TestsFlextWebUtilities.Web.Tests._wrap_result(
                            t.create_web_response(settings),
                        )
                    except (ValidationError, ValueError, TypeError) as exc:
                        return r[BaseModel].fail(str(exc))
                if entry_type == "application":
                    name = kwargs.get("name")
                    host = kwargs.get("host")
                    port = kwargs.get("port")
                    status = kwargs.get("status")
                    if (
                        not isinstance(name, str)
                        or not isinstance(host, str)
                        or not isinstance(port, int)
                    ):
                        return r[BaseModel].fail("Invalid parameters for application")
                    settings = t.Web.ApplicationConfig(
                        name=name,
                        host=host,
                        port=port,
                        status=status if isinstance(status, str) else "stopped",
                    )
                    return TestsFlextWebUtilities.Web.Tests._wrap_result(
                        t.create_application(settings),
                    )
                raise ValueError(f"Unsupported entry type: {entry_type}")

            @staticmethod
            def create_test_data(
                data_type: str,
                **kwargs: t.Scalar,
            ) -> dict[str, t.RecursiveContainer]:
                """Create centralized test data payloads."""
                if data_type == "app_data":
                    app_data: dict[str, t.RecursiveContainer] = {
                        "name": c.Web.Tests.TestWeb.TEST_APP_NAME,
                        "host": c.Web.Tests.TestWeb.DEFAULT_HOST,
                        "port": c.Web.Tests.TestWeb.DEFAULT_PORT,
                    }
                    app_data.update({k: v for k, v in kwargs.items() if u.primitive(v)})
                    return app_data
                if data_type == "entity_data":
                    entity_data: dict[str, t.RecursiveContainer] = {
                        "id": "test-entity",
                        "name": "Test Entity",
                    }
                    entity_data.update({
                        k: v for k, v in kwargs.items() if u.primitive(v)
                    })
                    return entity_data
                if data_type == "config_data":
                    config_data: dict[str, t.RecursiveContainer] = {
                        "host": c.Web.Tests.TestWeb.DEFAULT_HOST,
                        "port": c.Web.Tests.TestWeb.DEFAULT_PORT,
                        "debug": True,
                    }
                    config_data.update({
                        k: v for k, v in kwargs.items() if u.primitive(v)
                    })
                    return config_data
                if data_type == "request_data":
                    request_data: dict[str, t.RecursiveContainer] = {
                        "method": c.Web.Tests.TestHttp.TEST_METHOD,
                        "url": (
                            f"http://"
                            f"{c.Web.Tests.TestWeb.DEFAULT_HOST}:"
                            f"{c.Web.Tests.TestWeb.DEFAULT_PORT}"
                        ),
                        "headers": {
                            "Content-Type": (c.Web.Tests.TestHttp.TEST_CONTENT_TYPE)
                        },
                    }
                    request_data.update({
                        k: v for k, v in kwargs.items() if isinstance(v, (str, dict))
                    })
                    return request_data
                if data_type == "response_data":
                    response_data: dict[str, t.RecursiveContainer] = {
                        "status_code": 200,
                        "request_id": "test-123",
                    }
                    response_data.update({
                        k: v
                        for k, v in kwargs.items()
                        if isinstance(v, int | str | float | bool)
                    })
                    return response_data
                raise ValueError(f"Unsupported data type: {data_type}")

            @staticmethod
            def create_test_app(
                **kwargs: t.Scalar,
            ) -> m.Web.Entity:
                """Create a web test application entity."""
                defaults: dict[str, str | int] = {
                    "id": "test-id",
                    "name": c.Web.Tests.TestWeb.TEST_APP_NAME,
                    "host": c.Web.Tests.TestWeb.DEFAULT_HOST,
                    "port": c.Web.Tests.TestWeb.DEFAULT_PORT,
                }
                defaults.update({
                    k: v for k, v in kwargs.items() if isinstance(v, str | int)
                })
                id_value = defaults.get("id", "test-id")
                name_value = defaults.get(
                    "name",
                    c.Web.Tests.TestWeb.TEST_APP_NAME,
                )
                host_value = defaults.get(
                    "host",
                    c.Web.Tests.TestWeb.DEFAULT_HOST,
                )
                port_value = defaults.get(
                    "port",
                    c.Web.Tests.TestWeb.DEFAULT_PORT,
                )
                return m.Web.Entity(
                    id=id_value if isinstance(id_value, str) else "test-id",
                    name=(
                        name_value
                        if isinstance(name_value, str)
                        else c.Web.Tests.TestWeb.TEST_APP_NAME
                    ),
                    host=(
                        host_value
                        if isinstance(host_value, str)
                        else c.Web.Tests.TestWeb.DEFAULT_HOST
                    ),
                    port=(
                        port_value
                        if isinstance(port_value, int)
                        else c.Web.Tests.TestWeb.DEFAULT_PORT
                    ),
                )

            @staticmethod
            def create_test_result(
                *,
                success: bool = True,
                **kwargs: t.Scalar,
            ) -> p.Result[t.Scalar | None]:
                """Create standardized test results."""
                if success:
                    value: t.Scalar | None = kwargs.get("data") or kwargs.get("value")
                    return r[t.Scalar | None].ok(value)
                error = str(kwargs.get("error", "Test error"))
                return r[t.Scalar | None].fail(error)

            @staticmethod
            def run_parameterized_test(
                test_cases: Sequence[tuple[t.RecursiveContainer, ...]],
                test_function: Callable[..., p.Result[BaseModel]],
                expected_results: Sequence[bool],
                test_name: str = "parameterized_test",
            ) -> None:
                """Run standardized parameterized test cases."""
                for index, (test_case, expected_success) in enumerate(
                    zip(test_cases, expected_results, strict=True),
                ):
                    try:
                        result = test_function(*test_case)
                        if expected_success:
                            TestsFlextWebUtilities.Web.Tests.assert_success(
                                result,
                                f"{test_name} case {index} should succeed",
                            )
                        else:
                            TestsFlextWebUtilities.Web.Tests.assert_failure(
                                result,
                                f"{test_name} case {index} should fail",
                            )
                    except (
                        ValidationError,
                        ValueError,
                        TypeError,
                        RuntimeError,
                    ) as exc:
                        pytest.fail(
                            f"{test_name} case {index} raised unexpected exception: {exc}",
                        )

            @staticmethod
            def create_comprehensive_test_suite(
                entity_type: str,
                valid_cases: Sequence[t.ScalarMapping],
                invalid_cases: Sequence[t.ScalarMapping],
                test_name_prefix: str = "comprehensive",
            ) -> None:
                """Run comprehensive valid/invalid case suites."""
                for index, params in enumerate(valid_cases):
                    test_name = f"{test_name_prefix}_valid_case_{index}"
                    result = TestsFlextWebUtilities.Web.Tests.create_entry(
                        entity_type,
                        **params,
                    )
                    TestsFlextWebUtilities.Web.Tests.assert_success(
                        result,
                        f"{test_name} should succeed",
                    )
                for index, params in enumerate(invalid_cases):
                    test_name = f"{test_name_prefix}_invalid_case_{index}"
                    result = TestsFlextWebUtilities.Web.Tests.create_entry(
                        entity_type,
                        **params,
                    )
                    TestsFlextWebUtilities.Web.Tests.assert_failure(
                        result,
                        f"{test_name} should fail",
                    )


u = TestsFlextWebUtilities
__all__: list[str] = ["TestsFlextWebUtilities", "u"]
