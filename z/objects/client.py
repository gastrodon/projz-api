from __future__ import annotations
import os, types
from .zthing import ZThing
from .. import objects

class Client(ZThing):
    raw_device_id: str = os.environ.get("Z_RAW_DEVICE_ID", "")
    os_type: str = "2"
    device_type: str = "1"

    def __init__(self, data: dict[str, any] = {}, sid: str = None) -> Client:
        super().__init__(client = self, data = data)
        self._sid: str = sid
        self._secret: str = None

        self._profile: Profile = None
        self._profile_data: dict[str, any] = {}

    @property
    def headers(self):
        return {
            "rawDeviceId": self.raw_device_id,
            "osType": self.os_type,
            "deviceType": self.device_type,
            "sId": self._sid if self._sid else "",
        }

    @property
    def email(self) -> str:
        return self.get("email")

    @property
    def created(self) -> int:
        return self.get("createdTime")

    @property
    def device_id(self) -> str:
        return self.get("deviceId")

    @property
    def has_profile(self) -> bool:
        return self.get("hasProfile", casted = bool)

    async def _get_self_profile(self) -> Profile:
        if not self._sid and not self._profile:
            return None

        if not self._profile or self._fresh:
            from ..objects import Profile
            self._profile = Profile(self.id, client = self, data = self._profile_data)

        return self._profile

    @property
    def profile(self):
        return self._get_self_profile()

    @property
    def alerts(self) -> dict[str, int]:
        return self.request_route("GET", "/alerts/check")

    async def login(self, email: str = None, phone: str = None, security_code: str = None, *, password: str) -> Client:
        if not email or phone:
            raise ValueError("An email or phone is required")

        data: dict[str, str] = {
            "authType": 1 if email else 2,
            "password": password,
            "email": email if email else "",
            "phoneNumber": phone if phone else "",
            "securityCode": security_code if security_code else ""
        }

        response: dict[str, any] = await self.request_route("POST", "/auth/login", json = data)
        self._sid = response["sId"]
        self._secret = response["secret"]
        self._data = response["account"]
        self._profile_data = response["userProfile"]

        self.id = await self.get("uid")
        return self

    def namecards_slice(self, size: int = 30, page: str = None, gender: str = None) -> dict[str, any]:
        from ..objects import Profile
        return self.request_paged_route(
            "GET",
            "/users/namecards",
            size = size, page = page,
            transformer = lambda it : Profile(it["uid"], data = it, client = self),
            params = { "gender": { "male": 0, "female": 1 }[gender] } if gender else {},
        )

    def blogs_slice(self, size: int = 30, page: str = None, type: str = "latest") -> dict[str, any]:
        from .blog import Blog
        return self.request_paged_route(
            "GET",
            "/blogs",
            size = size, page = page,
            transformer = lambda it : Blog(it["blogId"], data = it, client = self),
            params = { "type": "latest" },
        )

    @property
    def namecards(self) -> generator[Profile]:
        from ..objects import Profile
        return self.paged_generator(
            "GET",
            "/users/namecards",
            transformer = lambda it : Profile(it["uid"], data = it, client = self)
        )

    @property
    def blogs(self) -> Namespace[generator[Blog]]:
        from .blog import Blog
        transformer: function = lambda it : Blog(it["blogId"], data = it, client = self)

        return types.SimpleNamespace(
            latest = self.paged_generator(
                "GET", "/blogs", params = { "type": "latest" },
                transformer = transformer,
            ),

            following = self.paged_generator(
                "GET", "/blogs", params = { "type": "following" },
                transformer = transformer,
            ),
        )
