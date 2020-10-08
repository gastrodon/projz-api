from __future__ import annotations
from .zthing import ZThing

class Circle(ZThing):
    def __init__(self, id: str, **kwargs):
        super().__init__(**kwargs)
        self.id = id
        self._route = f"/circles/{self.id}"
