from __future__ import annotations
import os, unittest
import z

class TestProfile(unittest.IsolatedAsyncioTestCase):
    async def asyncSetUp(self):
        self.email = os.environ["Z_TEST_EMAIL"]
        self.password = os.environ["Z_TEST_PASSWORD"]
        self.client = await z.Client().login(email = self.email, password = self.password)
        self.profile = await self.client.profile

    async def test_getters(self):
        assert await self.profile.gender in {"male", "female", "other"}
        assert {
            0: "female",
            1: "male"
        }.get(await self.profile.get("gender"), "other") == await self.profile.gender

        assert isinstance(await self.profile.content_region_name, str)
        assert isinstance(await self.profile.nickname, str)
        assert isinstance(await self.profile.school, str)
        assert isinstance(await self.profile.social_id, str)

        assert isinstance(await self.profile.social_id_modified, bool)
        assert isinstance(await self.profile.name_card_enabled, bool)
        assert isinstance(await self.profile.push_enabled, bool)
        assert isinstance(await self.profile.shows_joined_circles, bool)
        assert isinstance(await self.profile.shows_location, bool)
        assert isinstance(await self.profile.shows_school, bool)

        assert isinstance(await self.profile.content_region, int)
        assert isinstance(await self.profile.chat_invitation_status, int)
        assert isinstance(await self.profile.created, int)
        assert isinstance(await self.profile.fan_count, int)
        assert isinstance(await self.profile.following_count, int)
        assert isinstance(await self.profile.online_status, int)

        assert isinstance(await self.profile.icon, dict)
        assert isinstance(await self.profile.location, dict)

        assert await self.profile.has_profile == True
