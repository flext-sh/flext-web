# AUTO-GENERATED FILE — Regenerate with: make gen
"""Flext Web. Constants package.

Copyright (c) 2026 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from typing import TYPE_CHECKING

from flext_core.lazy import install_lazy_exports

if TYPE_CHECKING:
    from flext_web._constants.base import FlextWebConstantsBase
    from flext_web._constants.values import FlextWebConstantsValues


__all__: tuple[str, ...] = ("FlextWebConstantsBase", "FlextWebConstantsValues")

install_lazy_exports(
    __name__,
    globals(),
    {"FlextWebConstantsBase": ".base", "FlextWebConstantsValues": ".values"},
    public_exports=__all__,
    deferred_members={
        "FlextWebConstantsBase": (
            "VALIDATION_NAME_LENGTH_RANGE",
            "SECURITY_MAX_DESCRIPTION_LENGTH",
            "API_DOCS_URL",
            "API_REDOC_URL",
            "API_OPENAPI_URL",
            "API_DEFAULT_DESCRIPTION",
        ),
        "FlextWebConstantsValues": (
            "SUCCESS_RANGE",
            "ERROR_MIN",
            "ENVIRONMENTS",
            "SLUG_NON_WORD_RE",
            "SLUG_SPLIT_RE",
            "Method",
            "StatusCode",
            "ApplicationType",
            "ResponseStatus",
            "Name",
            "Status",
            "STATUSES",
            "DEFAULT_TIMEOUT_SECONDS",
            "DEFAULT_HTTP_PROTOCOL",
            "DEFAULT_HTTPS_PROTOCOL",
            "SERVICE_NAME",
            "SERVICE_NAME_API",
            "ALL_INTERFACES",
            "LOCALHOST_IP",
            "SYSTEM_PORTS_THRESHOLD",
            "PRIVILEGED_PORTS_MAX",
            "VALIDATION_PORT_RANGE",
            "VALIDATION_MAX_CONTENT_LENGTH_DEFAULT",
            "VALIDATION_MIN_CONTENT_LENGTH",
            "VALIDATION_REQUEST_TIMEOUT_DEFAULT",
            "VALIDATION_REQUEST_TIMEOUT_MAX",
            "VALIDATION_MAX_URL_LENGTH",
            "VALIDATION_MIN_URL_LENGTH",
            "VALIDATION_MAX_HEADER_LENGTH",
            "VALIDATION_MAX_HEADERS_COUNT",
            "VALIDATION_CONTENT_LENGTH_RANGE",
            "VALIDATION_REQUEST_TIMEOUT_RANGE",
            "VALIDATION_URL_LENGTH_RANGE",
            "HTTP_CONTENT_TYPE_JSON",
            "SECURITY_MIN_SECRET_KEY_LENGTH",
            "SECURITY_RESERVED_NAMES",
            "SECURITY_DANGEROUS_PATTERNS",
            "SECURITY_CORS_DEFAULT_ORIGINS",
            "SECURITY_CORS_SAFE_METHODS",
            "SECURITY_CORS_SAFE_HEADERS",
            "SECURITY_SESSION_DEFAULTS",
            "SECURITY_SSL_PORTS",
            "SECURITY_SSL_ALT_PORT",
            "SECURITY_SESSION_COOKIE_SECURE_DEFAULT",
            "SECURITY_SESSION_COOKIE_HTTPONLY_DEFAULT",
            "SECURITY_SESSION_COOKIE_SAMESITE_DEFAULT",
            "SECURITY_MAX_HOST_LENGTH",
            "FRAMEWORK_INTERFACE_ASGI",
            "FRAMEWORK_INTERFACE_WSGI",
            "FRAMEWORK_RUNNER_UVICORN",
            "FRAMEWORK_FASTAPI",
            "ACTION_CREATE",
            "ACTION_START",
            "ACTION_STOP",
            "ACTION_LIST",
            "MESSAGE_CONFIG_LOADED",
            "MESSAGE_HANDLERS_REGISTERED",
        ),
    },
)
