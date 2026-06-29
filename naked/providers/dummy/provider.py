from naked.models.search_result import SearchResult
from naked.core.plugin import Provider

class DummyProvider(Provider):

    name = "dummy"

    async def search(self, username: str) -> SearchResult:

        return SearchResult(
            provider=self.name,
            username=username,
            exists=True,
            url=f"https://dummy.local/{username}",
        )