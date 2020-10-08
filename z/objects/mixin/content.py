from __future__ import annotations

class Content:
    @property
    def content_region(self) -> int:
        return self.get("contentRegion")

    @property
    def content_region_name(self) -> str:
        return self.get("contentRegionName")

    @property
    def icon(self) -> dict[str, any]:
        return self.get("icon")

    @property
    def language(self) -> str:
        return self.get("language")

    @property
    def social_id(self) -> str:
        return self.get("socialId")

    @property
    def social_id_modified(self) -> bool:
        return self.get("socialIdModified", casted = lambda it : it != 2)

    @property
    def created(self) -> int:
        return self.get("createdTime")
