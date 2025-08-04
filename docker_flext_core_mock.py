# Minimal flext-core mock for standalone Docker operation
import logging
from typing import Any, Generic, TypeVar

from pydantic import BaseModel

T = TypeVar("T")


class FlextResult[T]:
    def __init__(self, success: bool, data: T | None = None, error: str | None = None) -> None:
        self._success = success
        self._data = data
        self._error = error

    @property
    def is_success(self) -> bool:
        return self._success

    @property
    def is_failure(self) -> bool:
        return not self._success

    @property
    def data(self) -> T | None:
        return self._data

    @property
    def error(self) -> str | None:
        return self._error

    @classmethod
    def ok(cls, data: T | None = None):
        return cls(True, data)

    @classmethod
    def fail(cls, error: str):
        return cls(False, None, error)


class FlextEntity(BaseModel):
    id: str


class FlextTimestampMixin(BaseModel):
    created_at: str | None = None
    updated_at: str | None = None


class FlextValidatableMixin(BaseModel):
    def validate_domain_rules(self) -> FlextResult[None]:
        return FlextResult.ok(None)


class FlextConfig(BaseModel):
    pass


class FlextError(Exception):
    pass


class FlextValidationError(FlextError):
    pass


class FlextValidators:
    @staticmethod
    def is_non_empty_string(value: Any) -> bool:
        return isinstance(value, str) and len(value.strip()) > 0

    @staticmethod
    def is_valid_port(port: int) -> bool:
        return isinstance(port, int) and 1 <= port <= 65535

    @staticmethod
    def matches_pattern(value: str, pattern: str) -> bool:
        import re

        return bool(re.match(pattern, value))


U = TypeVar("U")


class FlextHandlers:
    class Handler(Generic[T, U]):
        pass


def get_logger(name: str) -> logging.Logger:
    return logging.getLogger(name)
