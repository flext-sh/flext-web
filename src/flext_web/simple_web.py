"""Simple Web Components."""

from __future__ import annotations

from typing import Any

from flext_core import FlextResult


def create_response(data: Any, status: int = 200) -> dict[str, Any]:
    """Create standardized response."""
    return {"status": status, "data": data, "success": status < 400}


def create_error_response(message: str, status: int = 400) -> dict[str, Any]:
    """Create error response."""
    return {"status": status, "error": message, "success": False}


def create_success_response(data: Any, message: str = "Success") -> dict[str, Any]:
    """Create success response."""
    return {"status": 200, "data": data, "message": message, "success": True}


def validate_request_data(
    data: dict[str, Any],
    required_fields: list[str],
) -> FlextResult[bool]:
    """Validate request data has required fields."""
    try:
        missing_fields = [field for field in required_fields if field not in data]

        if missing_fields:
            return FlextResult.fail(
                f"Missing required fields: {', '.join(missing_fields)}",
            )

        return FlextResult.ok(True)
    except Exception as e:
        return FlextResult.fail(f"Validation failed: {e}")


def format_pagination(page: int, page_size: int, total: int) -> dict[str, Any]:
    """Format pagination metadata."""
    return {
        "page": page,
        "page_size": page_size,
        "total": total,
        "total_pages": (total + page_size - 1) // page_size,
        "has_next": page * page_size < total,
        "has_previous": page > 1,
    }


class FlextSimpleTemplate:
    """Simple template renderer."""

    def __init__(self, template_string: str) -> None:
        self.template = template_string

    def render(self, context: dict[str, Any]) -> FlextResult[str]:
        """Render template with context."""
        try:
            rendered = self.template.format(**context)
            return FlextResult.ok(rendered)
        except KeyError as e:
            return FlextResult.fail(f"Missing template variable: {e}")
        except Exception as e:
            return FlextResult.fail(f"Template rendering failed: {e}")


def create_template(template_string: str) -> FlextSimpleTemplate:
    """Create a simple template."""
    return FlextSimpleTemplate(template_string)
