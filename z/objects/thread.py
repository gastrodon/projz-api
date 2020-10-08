from __future__ import annotations
from .zthing import ZThing
from .mixin import Content

class Thread(ZThing, Content):
    def __init__(self,  id: str, **kwargs):
        super().__init__(**kwargs)
        self.id = id
        self._route = f"/chat/threads/{self.id}"
