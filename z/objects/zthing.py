from __future__ import annotations
import os, json
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

    async def request(self, *args, **kwargs) -> dict[str, any]:
        kwargs["headers"] = {
            **self.client.headers,
            **kwargs.get("headers", {}),
        }

        async with httpx.AsyncClient() as client:
            response: httpx.response = await client.request(*args, **kwargs)


        try:
            data: dict[str, any] = response.json()
            if 200 <= response.status_code <= 299:
                return data

            raise exceptions.APIException(data["debugMsg"], api_code = data["apiCode"])
        except (json.decoder.JSONDecodeError, KeyError):
            raise exceptions.APIException(f"{response.status_code}: {response.text}", api_code = 0)

    def request_route(self, method: str, route: str, *args, **kwargs) -> httpx.response:
        return self.request(method, f"{self.api}{route}", *args, **kwargs)

    async def request_paged_route(
        self, method: str, route: str, transformer: function = noop,
        size: int = 30, page: str = None, **kwargs
    ) -> dict[str, any]:
        response: dict[str, any] = await self.request_route(
            method, route,
            params = { "size": size, "pageToken": page, **kwargs.get("params", {}) },
        )

        return {
            "data": [ transformer(it) for it in response["list"] ],
            "page": response.get("pagination", {}).get("nextPageToken"),
        }

    async def paged_generator(self, method: str, route: str, transformer: function = noop) -> generator[any]:
        page: str = None

        while True:
            buffer: dict[str, any] = await self.request_paged_route(method, route, transformer = transformer, page = page)
            for it in buffer["data"]:
                yield it

            page = buffer["page"]
            if not page:
                return

    async def get(self, key: str, default: any = None, *, casted: any = noop) -> any:
        if (fetched := (await self.data).get(key)) != None:
            return casted(fetched)

        return casted((await self.fresh.data).get(key, default))

    @property
    def fresh(self) -> ZThing:
        self._fresh = True
        return self

    @property
    def data(self) -> dict[str, any]:
        return self._async_data()

    async def _get_uid(self) -> str:
        return self.id

    @property
    def uid(self) -> str:
        return self._get_uid()

    @property
    def status(self) -> int:
        return self.get("status")
