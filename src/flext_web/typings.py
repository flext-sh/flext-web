"""Centralized typings facade for flext-web.

This module consolidates all web-specific type aliases and protocols,
extending flext-core types while providing a single FlextWebTypes class
following the "one class per module" architectural requirement.
"""

from __future__ import annotations

from collections.abc import Callable, Generator
from typing import TypedDict

from flext_core import E, F, FlextTypes as CoreFlextTypes, P, R, T, U, V


class FlextWebTypes(CoreFlextTypes):
    """Consolidated web domain-specific types extending flext-core patterns.

    This class serves as the single point of access for all web-specific
    type aliases, consolidating functionality from multiple modules while
    maintaining proper inheritance from flext-core types.
    """

    # =========================================================================
    # FIELD AND VALIDATION TYPES
    # =========================================================================

    class FieldKwargs(TypedDict, total=False):
        """Type-safe kwargs for Pydantic Field() function."""

        alias: str | None
        alias_priority: int | None
        validation_alias: str | None
        serialization_alias: str | None
        title: str | None
        description: str | None
        examples: list[object] | None
        exclude: bool | None
        deprecated: str | None
        json_schema_extra: dict[str, object] | None
        frozen: bool | None
        validate_default: bool | None
        repr: bool | None
        init: bool | None
        init_var: bool | None
        kw_only: bool | None
        pattern: str | None
        strict: bool | None
        coerce_numbers_to_str: bool | None
        gt: float | None
        ge: float | None
        lt: float | None
        le: float | None
        multiple_of: float | None
        allow_inf_nan: bool | None
        max_digits: int | None
        decimal_places: int | None
        min_length: int | None
        max_length: int | None
        default: object

    # =========================================================================
    # CALLABLE AND GENERATOR TYPES
    # =========================================================================

    ValidatorFunc = Callable[[object], object]
    ValidatorGenerator = Generator[ValidatorFunc]

    # =========================================================================
    # WEB-SPECIFIC REQUEST/RESPONSE TYPES
    # =========================================================================

    RequestContext = dict[str, object]
    ResponseData = str | int | float | bool | dict[str, object] | list[object] | None
    TemplateContext = object
    ConfigValue = str | int | float | bool | dict[str, object] | list[object] | None
    ConfigDict = dict[str, ConfigValue]
    ErrorDetails = dict[str, object] | None
    SchemaDict = dict[str, object]

    # Template-specific types
    TemplateFilter = Callable[[object], object]
    TemplateGlobal = object
    HTTPStatus = int

    # =========================================================================
    # API RESPONSE STRUCTURE TYPES
    # =========================================================================

    class AppDataDict(TypedDict):
        """Type definition for application data in API responses."""

        name: str
        host: str
        port: int
        status: str
        id: str

    class ResponseDataDict(TypedDict):
        """Type definition for generic response data structure."""

        success: bool
        message: str
        data: dict[str, object] | list[object] | None
        errors: dict[str, object] | None

    class ApiResponseDict(TypedDict):
        """Type definition for structured API response format."""

        success: bool
        message: str
        data: dict[str, object] | list[object] | None

    class AppListDataDict(TypedDict):
        """Type definition for application list data in API responses."""

        apps: list[AppDataDict]

    class AppListResponseDict(TypedDict):
        """Type definition for application list API response structure."""

        success: bool
        message: str
        data: AppListDataDict

    class HealthResponseDict(TypedDict):
        """Type definition for health check response structure."""

        success: bool
        message: str
        data: HealthDataDict

    class HealthDataDict(TypedDict):
        """Type definition for health check data structure."""

        status: str
        service: str
        version: str
        apps_count: int


# =========================================================================
# LEGACY COMPATIBILITY ALIASES
# =========================================================================

# Maintain backward compatibility while encouraging use of consolidated class
FlextTypes = FlextWebTypes  # Legacy alias
FieldKwargs = FlextWebTypes.FieldKwargs
ValidatorFunc = FlextWebTypes.ValidatorFunc
ValidatorGenerator = FlextWebTypes.ValidatorGenerator
RequestContext = FlextWebTypes.RequestContext
ResponseData = FlextWebTypes.ResponseData
TemplateContext = FlextWebTypes.TemplateContext
ConfigValue = FlextWebTypes.ConfigValue
ConfigDict = FlextWebTypes.ConfigDict
ErrorDetails = FlextWebTypes.ErrorDetails
SchemaDict = FlextWebTypes.SchemaDict
TemplateFilter = FlextWebTypes.TemplateFilter
TemplateGlobal = FlextWebTypes.TemplateGlobal
HTTPStatus = FlextWebTypes.HTTPStatus
AppDataDict = FlextWebTypes.AppDataDict
ResponseDataDict = FlextWebTypes.ResponseDataDict
ApiResponseDict = FlextWebTypes.ApiResponseDict
AppListDataDict = FlextWebTypes.AppListDataDict
AppListResponseDict = FlextWebTypes.AppListResponseDict
HealthResponseDict = FlextWebTypes.HealthResponseDict
HealthDataDict = FlextWebTypes.HealthDataDict


__all__ = [
    "ApiResponseDict",
    "AppDataDict",
    "AppListDataDict",
    "AppListResponseDict",
    "ConfigDict",
    "ConfigValue",
    # Core type exports
    "E",
    "ErrorDetails",
    "F",
    # Type aliases for direct access
    "FieldKwargs",
    # Legacy compatibility
    "FlextTypes",
    # Main consolidated class
    "FlextWebTypes",
    "HTTPStatus",
    "HealthDataDict",
    "HealthResponseDict",
    "P",
    "R",
    "RequestContext",
    "ResponseData",
    "ResponseDataDict",
    "SchemaDict",
    "T",
    "TemplateContext",
    "TemplateFilter",
    "TemplateGlobal",
    "U",
    "V",
    "ValidatorFunc",
    "ValidatorGenerator",
]
