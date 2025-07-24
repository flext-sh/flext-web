"""FLEXT Web Interface - Enterprise FlexCore Management Dashboard."""

from __future__ import annotations

from .api import FlextWebAPI, create_app
from .simple_web import (
    SimpleTemplate,
    create_error_response,
    create_response,
    create_template,
    format_pagination,
    validate_request_data,
)
from .web_interface import FlexCoreManager

__version__ = "1.0.0"

__all__ = [
    "FlexCoreManager",
    "FlextWebAPI",
    "SimpleTemplate",
    "create_app",
    "create_error_response",
    "create_response",
    "create_template",
    "format_pagination",
    "validate_request_data",
]
