from __future__ import annotations
import os, unittest
import z

class TestCircle(unittest.IsolatedAsyncioTestCase):
    async def asyncSetUp(self):
        self.email = os.environ["Z_TEST_EMAIL"]
        self.password = os.environ["Z_TEST_PASSWORD"]
        self.client = await z.Client().login(email = self.email, password = self.password)
        self.circle = (await self.client.circles_slice())["data"][0]

    async def test_getters(self):
        assert isinstance(await self.circle.author, z.Profile)

        for profile in await self.circle.admins:
            assert isinstance(profile, z.Profile)

        assert isinstance(await self.circle.name, str)
        assert isinstance(await self.circle.description, str)
        assert isinstance(await self.circle.tagline, str)

        assert isinstance(await self.circle.background, dict)

        assert isinstance(await self.circle.tags, list)

        # Content getters
        assert isinstance(await self.circle.content_region, int)
        assert isinstance(await self.circle.created, int)

        # see z.mixin.Content.content_region_name comment
        # assert isinstance(await self.circle.content_region_name, str)
        assert isinstance(await self.circle.language, str)
        assert isinstance(await self.circle.social_id, str)

        assert isinstance(await self.circle.social_id_modified, bool)

        assert isinstance(await self.circle.icon, dict)
