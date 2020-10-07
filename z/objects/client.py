from __future__ import annotations
from .zthing import ZThing
from .. import objects

class Client(ZThing):
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
    def create_time(self) -> int:
        return self.get("createTime")

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

    def namecard_slice(self, size: int = 30, page: str = None) -> dict[str, any]:
        from ..objects import Profile
        return self.request_paged_route(
            "GET",
            "/users/namecards",
            size = size, page = page,
            transformer = lambda it : Profile(it["uid"], data = it, client = self)
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
    def alerts(self) -> dict[str, int]:
        return self.request_route("GET", "/alerts/check")
