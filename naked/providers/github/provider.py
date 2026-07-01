import httpx

from naked.core.exceptions import ProviderUnavailableError, RateLimitError
from naked.core.plugin import Provider
from naked.intelligence.score import ScoreCalculator
from naked.models.profiles.github import GithubProfile
from naked.models.search_result import ResultStatus, SearchResult
from typing import Any


class GithubProvider(Provider):
    name = "github"
    API_URL = "https://api.github.com/users"

    async def search(self, username: str) -> SearchResult:
        try:
            data = await self._fetch_user(username)
        except (RateLimitError, ProviderUnavailableError) as e:
            return self._build_error_result(username, str(e))
        return self._build_result(username, data)

    async def _fetch_user(self, username: str) -> dict[str, Any] | None:
        url = f"{self.API_URL}/{username}"
        headers = {"User-Agent": "NAKED/2.0"}

        try:
            async with httpx.AsyncClient(timeout=10, headers=headers) as client:
                response = await client.get(url)
        except httpx.TimeoutException as e:
            raise ProviderUnavailableError(f"GitHub timeout: {e}") from e
        except httpx.RequestError as e:
            raise ProviderUnavailableError(f"GitHub network error: {e}") from e

        if response.status_code == 404:
            return None
        if response.status_code == 429:
            raise RateLimitError("GitHub rate limit exceeded (429)")
        if response.status_code == 403:
            remaining = response.headers.get("X-RateLimit-Remaining")
            if remaining == "0":
                raise RateLimitError("GitHub rate limit exceeded (403)")
            raise ProviderUnavailableError("GitHub blocked the request (403)")
        if response.status_code >= 500:
            raise ProviderUnavailableError(f"GitHub server error ({response.status_code})")

        response.raise_for_status()
        return response.json()

    def _build_profile(self, data: dict[str, Any]) -> GithubProfile:
        return GithubProfile(
            display_name=data.get("name"),
            avatar_url=data.get("avatar_url"),
            bio=data.get("bio"),
            company=data.get("company"),
            location=data.get("location"),
            website=data.get("blog") or None,
            followers=data.get("followers"),
            following=data.get("following"),
            repositories=data.get("public_repos"),
        )

    def _build_result(self, username: str, data: dict[str, Any] | None) -> SearchResult:
        if data is None:
            return SearchResult(
                provider=self.name,
                username=username,
                exists=False,
                status=ResultStatus.NOT_FOUND,
                url=f"https://github.com/{username}",
            )

        profile = self._build_profile(data)
        result = SearchResult(
            provider=self.name,
            username=username,
            exists=True,
            status=ResultStatus.FOUND,
            url=data.get("html_url"),
            profile=profile,
            raw=data,
        )
        result.score = ScoreCalculator.calculate(result)
        return result

    def _build_error_result(self, username: str, error: str) -> SearchResult:
        return SearchResult(
            provider=self.name,
            username=username,
            exists=False,
            status=ResultStatus.ERROR,
            error=error,
            url=f"https://github.com/{username}",
        )