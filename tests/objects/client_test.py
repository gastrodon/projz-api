from __future__ import annotations
import os, unittest
import z
import z.ext.exceptions as exceptions

class TestClient(unittest.IsolatedAsyncioTestCase):
    async def asyncSetUp(self):
        self.email = os.environ["Z_TEST_EMAIL"]
        self.password = os.environ["Z_TEST_PASSWORD"]
        self.client = await z.Client().login(email = self.email, password = self.password)

    async def test_headers(self):
        assert self.client.headers["sId"] == self.client._sid != None
        assert self.client.headers["osType"] == self.client.os_type != None
        assert self.client.headers["deviceType"] == self.client.device_type != None
        assert self.client.headers["rawDeviceId"] == self.client.raw_device_id != None

    async def test_takes_sid(self):
        sid: str = "foobar"
        client = z.Client(sid = sid)
        assert client._sid == sid

    async def test_login(self):
        client: z.Client = await z.Client().login(email = self.email, password = self.password)
        assert client._sid != None

    async def test_login_fails(self):
        with self.assertRaises(TypeError):
            await z.Client().login(email = "foo@bar.io")

        with self.assertRaises(TypeError):
            await z.Client().login(phone = "+1 666 420 6969")

        with self.assertRaises(ValueError):
            await z.Client().login(password = "foobar2000")

    async def test_properties(self):
        assert await self.client.email == self.email
        assert await self.client.has_profile == True

        assert isinstance(await self.client.created, int)
        assert isinstance(await self.client.device_id, str)
        assert isinstance(await self.client.profile, z.Profile)
        assert isinstance(await self.client.alerts, dict)

    async def test_namecards_slice(self):
        size: int = 5
        slice: dict[str, any] = await self.client.namecards_slice(size = size)
        assert len(slice["data"]) == size
        assert isinstance(slice["data"][0], z.Profile)

        next_slice: dict[str, any] = await self.client.namecards_slice(size = size, page = slice["page"])
        assert next_slice["data"][0].id != slice["data"][0].id

    async def test_blogs_slice(self):
        size: int = 5
        slice: dict[str, any] = await self.client.blogs_slice(size = size)
        assert len(slice["data"]) == size
        assert isinstance(slice["data"][0], z.Blog)

        next_slice: dict[str, any] = await self.client.blogs_slice(size = size, page = slice["page"])
        assert next_slice["data"][0].id != slice["data"][0].id

    async def test_circles_slice(self):
        size: int = 5
        slice: dict[str, any] = await self.client.circles_slice(size = size)
        assert len(slice["data"]) == size
        assert isinstance(slice["data"][0], z.Circle)

        next_slice: dict[str, any] = await self.client.circles_slice(size = size, page = slice["page"])
        assert next_slice["data"][0].id != slice["data"][0].id


    async def test_namecards(self):
        index: int = 0
        size: int = 50
        collection: list[Blog] = []

        async for blog in self.client.namecards:
            collection.append(blog)

            if size == (index := index + 1):
                break

        assert len(collection) == size
        assert len(collection) == len(set([it.id for it in collection]))

    async def test_blogs(self):
        index: int = 0
        size: int = 50
        collection: list[Blog] = []

        async for blog in self.client.blogs.latest:
            collection.append(blog)

            if size == (index := index + 1):
                break

        assert len(collection) == size
        assert len(collection) == len(set([it.id for it in collection]))
