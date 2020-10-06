from __future__ import annotations
import os
import httpx
from ..ext import exceptions

noop: function = lambda _ : _

class ZThing:
    api: str = "https://api.projz.com/v1"
    raw_device_id: str = os.environ.get("Z_RAW_DEVICE_ID", "")
    os_type: str = "2"
    device_type: str = "1"

    def __init__(self, client: Client = None, data: dict[str, any] = {}) -> ZThing:
        self.client = client if client else __import__("client")
        self._data = data
        self._fresh = False

        self.id = ""
        self._route = ""

    async def _async_data(self) -> dict[str, any]:
        if self._fresh:
            self._fresh = False
            self._data = await self.request_route("GET", self._route)

        return self._data

    async def request(self, *args, **kwargs) -> httpx.response:
        kwargs["headers"] = {
            **self.client.headers,
            **kwargs.get("headers", {}),
        }

        async with httpx.AsyncClient() as client:
            response: httpx.response = await client.request(*args, **kwargs)

        if 200 <= response.status_code <= 299:
            return response.json()

        raise exceptions.APIException(response.json().get("apiMsg", response.text))

    def request_route(self, method: str, route: str, *args, **kwargs) -> httpx.response:
        return self.request(method, f"{self.api}{route}", *args, **kwargs)

    async def get(self, key: str, default: any = None, *, casted: any = noop) -> any:
        if (fetched := (await self.data).get(key)) != None:
            return casted(fetched)

        return (await self.fresh.data).get(key, default, casted = casted)

    @property
    def fresh(self) -> ZThing:
        self._fresh = True
        return self

    @property
    def data(self) -> dict[str, any]:
        return self._async_data()

    @property
    def uid(self) -> str:
        return self.id
