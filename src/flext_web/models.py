"""FLEXT Web model facade."""

from __future__ import annotations

from flext_cli import FlextCliModels

from flext_web import t

from ._models._auth import FlextWebModelsAuth
from ._models._base import FlextWebModelsBase
from ._models._config import FlextWebModelsConfig
from ._models._entity import FlextWebModelsEntity
from ._models._factory import FlextWebModelsFactory
from ._models._http import FlextWebModelsHttp
from ._models._responses import FlextWebModelsResponses
from ._models._system import FlextWebModelsSystem
from ._models._web_message import FlextWebModelsWebMessage
from ._models._web_request import FlextWebModelsWebRequest


class FlextWebModels(FlextCliModels):
    """HTTP domain models for flext-web."""

    class Web(
        FlextWebModelsBase,
        FlextWebModelsConfig,
        FlextWebModelsEntity,
        FlextWebModelsFactory,
        FlextWebModelsHttp,
        FlextWebModelsResponses,
        FlextWebModelsSystem,
        FlextWebModelsWebMessage,
        FlextWebModelsWebRequest,
        FlextWebModelsAuth,
    ):
        """Web domain models namespace."""


m = FlextWebModels

__all__: t.MutableSequenceOf[str] = ["FlextWebModels", "m"]
