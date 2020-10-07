from __future__ import annotations
import os, unittest
import z

class TestClient(unittest.IsolatedAsyncioTestCase):
    async def asyncSetUp(self):
        self.email = os.environ["Z_TEST_EMAIL"]
        self.password = os.environ["Z_TEST_PASSWORD"]
        self.client = await z.Client().login(email = self.email, password = self.password)
        # self.blog = (await self.client.blogs_slice(size = 1))["data"][0]
        async for blog in self.client.blogs.latest:
            if await blog.media:
                self.blog = blog
                break

    async def test_getters(self):
        assert isinstance(await self.blog.author, z.Profile)

        media: list[dict] = await self.blog.media
        assert all([ isinstance(it, dict) for it in media ])

        # TODO:
        # circles: list[Circle] = await self.blog.circles
        # assert all([ isinstance(it, z.Circle) for it in circles ])

        assert isinstance(await self.blog.content, str)
        assert isinstance(await self.blog.language, str)

        assert isinstance(await self.blog.content_region, int)
        assert isinstance(await self.blog.visibility, int)
        assert isinstance(await self.blog.type, int)
        assert isinstance(await self.blog.vote_count, int)
        assert isinstance(await self.blog.comment_count, int)
        assert isinstance(await self.blog.comment_count, int)
