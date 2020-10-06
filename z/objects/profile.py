from __future__ import annotations
from .zthing import ZThing
from .. import objects

class Profile(ZThing):
    def __init__(self, id: str, **kwargs):
        super().__init__(**kwargs)
        self.id = id
        self._route = f"/users/profile/{self.id}"

    @property
    def chat_invitation_status(self) -> int:
        # TODO: is this a bool?
        return self.get("chatInvitationStatus")

    @property
    def content_region(self) -> str:
        return self.get("contentRegion")

    @property
    def content_region_name(self) -> str:
        return self.get("contentRegionName")

    @property
    def created(self) -> int:
        return self.get("createdTime")

    @property
    def fan_count(self) -> int:
        return self.get("fansCount")

    @property
    def following_count(self) -> int:
        return self.get("followingCount")

    @property
    def friend_count(self) -> int:
        return self.get("friendsCount")

    @property
    def status(self) -> int:
        return self.get("status")

    @property
    def online_status(self) -> int:
        return self.get("onlineStatus")

    @property
    def gender(self) -> str:
        genders: dict[str, str] = {
            0: "female",
            1: "male",
        }
        return self.get("gender", casted = lambda it : genders.get(it, "other"))

    @property
    def icon(self) -> dict[str, any]:
        # TODO object to represent media
        return self.get("icon")

    @property
    def language(self) -> str:
        return self.get("language")

    @property
    def location(self) -> dict[str, any]:
        return self.get("location")

    @property
    def nickname(self) -> str:
        return self.get("nickname")

    @property
    def school(self) -> str:
        return self.get("school")

    @property
    def social_id(self) -> str:
        return self.get("socialId")

    @property
    def social_id_modified(self) -> bool:
        return self.get("socialIdModified", casted = lambda it : it != 2)

    @property
    def has_profile(self) -> bool:
        return self.get("hasProfile", casted = bool)

    @property
    def name_card_enabled(self) -> bool:
        return self.get("nameCardEnabled", casted = bool)

    @property
    def name_card_background(self) -> dict[str, any]:
        # TODO: media object
        return self.get("nameCardBackground")

    @property
    def push_enabled(self) -> bool:
        return self.get("pushEnabled", casted = bool)

    @property
    def shows_joined_circles(self) -> bool:
        return self.get("showsJoinedCircles", casted = bool)

    @property
    def shows_location(self) -> bool:
        return self.get("showsLocation", casted = bool)

    @property
    def shows_school(self) -> bool:
        return self.get("showsSchool", casted = bool)
