"""Type aliases and custom types for flext-web.

This module provides specific type aliases to reduce the use of typing.Any
and improve type safety throughout the web module.
"""

from __future__ import annotations

from collections.abc import Callable, Generator
from typing import TypedDict

# Field and validation types with proper Pydantic compatibility
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

ValidatorFunc = Callable[[object], object]
ValidatorGenerator = Generator[ValidatorFunc]

# Request/response types
RequestContext = dict[str, object]
ResponseData = dict[str, object] | list[object] | str | int | float | bool | None
TemplateContext = dict[str, object]

# Configuration types
ConfigValue = str | int | float | bool | None
ConfigDict = dict[str, ConfigValue]

# Error handling types
ErrorDetails = dict[str, object] | str | None

# Pydantic schema types (keeping Any for Pydantic compatibility)
SchemaDict = dict[str, object]  # Simplified for mypy compatibility

# Filter and template types
TemplateFilter = Callable[[object], str]
TemplateGlobal = object

# HTTP status codes
HTTPStatus = int

__all__ = [
    "ConfigDict",
    "ConfigValue",
    "ErrorDetails",
    "FieldKwargs",
    "HTTPStatus",
    "RequestContext",
    "ResponseData",
    "SchemaDict",
    "TemplateContext",
    "TemplateFilter",
    "TemplateGlobal",
    "ValidatorFunc",
    "ValidatorGenerator",
]
