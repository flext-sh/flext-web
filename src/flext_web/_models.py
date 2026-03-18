"""Auto-generated centralized models."""

from __future__ import annotations

from typing import TYPE_CHECKING

from pydantic import BaseModel, ConfigDict, RootModel

if TYPE_CHECKING:
    from threading import Thread
    from wsgiref.simple_server import WSGIServer

    import uvicorn


class FlextAutoConstants:
    pass


class FlextAutoTypes:
    pass


class FlextAutoProtocols:
    pass


class FlextAutoUtilities:
    pass


class FlextAutoModels:
    pass


c = FlextAutoConstants
t = FlextAutoTypes
p = FlextAutoProtocols
u = FlextAutoUtilities
m = FlextAutoModels


class AppRuntimeInfo(BaseModel):
    model_config = ConfigDict(extra="forbid")
    runner: str
    server: uvicorn.Server | WSGIServer
    thread: Thread


class WebRequestDict(
    RootModel[dict[str, str | int | bool | list[str] | dict[str, str | int | bool]]],
):
    pass


class WebResponseDict(
    RootModel[dict[str, str | int | bool | list[str] | dict[str, str | int | bool]]],
):
    pass
