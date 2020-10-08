from __future__ import annotations
from .zthing import ZThing
from .mixin import Content

class Circle(ZThing, Content):
    def __init__(self, id: str, **kwargs):
        super().__init__(**kwargs)
        self.id = id
        self._route = f"/circles/{self.id}"

    @property
    def author(self) -> Profile:
        from .profile import Profile
        return self.get(
            "author",
            casted = lambda it : Profile(it["uid"], data = it, client = self.client),
        )

    @property
    def admins(self) -> list[Profile]:
        from .profile import Profile
        return self.get(
            "adminIdList",
            casted = lambda it : [ Profile(id, client = self.client) for id in it ],
        )

    @property
    def name(self) -> str:
        return self.get("name")

    @property
    def description(self) -> str:
        return self.get("description")

    @property
    def tagline(self) -> str:
        return self.get("tagline")

    @property
    def joined_status(self) -> int:
        return self.get("joinedStatus")

    @property
    def background(self) -> dict[str, any]:
        return self.get("background")

    @property
    def tags(self) -> list[dict[str, any]]:
        # TODO: tag type
        return self.get("tagList")
