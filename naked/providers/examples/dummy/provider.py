from naked.core.plugin import Provider

from naked.models.profiles.base import BaseProfile

from naked.models.search_result import ResultStatus, SearchResult


class DummyProvider(Provider):

    name = "dummy"

    async def search(self, username):

        profile = BaseProfile(

            display_name="Dummy User",

            bio="Dummy provider"

        )

        return SearchResult(

            provider=self.name,

            username=username,

            exists=True,

            status=ResultStatus.FOUND,

            url=f"https://dummy.local/{username}",

            profile=profile
        )