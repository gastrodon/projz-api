from __future__ import annotations
from .zthing import ZThing
from .. import objects

class Profile(ZThing):
    def __init__(self, id: str, **kwargs):
        super().__init__(**kwargs)
        self.id = id
        self._route = f"/users/profile/{self.id}"
