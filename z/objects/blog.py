from __future__ import annotations
from .zthing import ZThing

class Blog(ZThing):
    def __init__(self, id: str, **kwargs):
        super().__init__(**kwargs)
        self.id = id
        self._route = f"/blogs/{self.id}"

    @property
    def blog_id(self) -> str:
        return self.get("blogId", casted = str)

    async def _get_author(self):
        data: map[str, any] = await self.get("author")

        from .profile import Profile
        return Profile(data["uid"], data = data, client = self)

    @property
    def author(self) -> Profile:
        return self._get_author()

    async def _get_circles(self) -> list[Circle]:
        # TODO:
        ...

    @property
    def circles(self) -> list[Circle]:
        return self._get_circles()

    @property
    def media(self) -> list[dict[str, any]]:
        return self.get("mediaList")

    @property
    def extensions(self) -> dict[str, any]:
        return self.get("extensions")

    @property
    def content(self) -> str:
        return self.get("content")

    @property
    def language(self) -> str:
        return self.get("language")

    @property
    def content_region(self) -> int:
        return self.get("contentRegion")

    @property
    def visibility(self) -> int:
        return self.get("visibility")

    @property
    def type(self) -> int:
        return self.get("type")

    @property
    def vote_count(self) -> int:
        return self.get("votesCount")

    @property
    def comment_count(self) -> int:
        return self.get("commentsCount")
