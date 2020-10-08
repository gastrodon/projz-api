from __future__ import annotations

class APIException(Exception):
    def __init__(self, *args, api_code: int = 0, response: response = None, **kwargs):
        super().__init__(*args, **kwargs)
        self.api_code = api_code
        self.response = response
