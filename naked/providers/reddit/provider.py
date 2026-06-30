import httpx

from naked.core.exceptions import ProviderUnavailableError, RateLimitError
from naked.core.plugin import Provider
from naked.intelligence.score import ScoreCalculator
from naked.models.profiles.reddit import RedditProfile
from naked.models.search_result import ResultStatus, SearchResult
from typing import Any


class RedditProvider(Provider):
    name = "reddit"

    API_URL = "https://www.reddit.com/user"

    async def search(self, username: str) -> SearchResult:
        try:
            data = await self._fetch_user(username)
        except (RateLimitError, ProviderUnavailableError) as e:
            return self._build_error_result(username, str(e))

        return self._build_result(username, data)

    async def _fetch_user(self, username: str) -> dict[str, Any] | None:
        """Obtiene la información del usuario desde el endpoint público de Reddit."""

        url = f"{self.API_URL}/{username}/about.json"

        headers = {
            # Reddit bloquea el User-Agent por defecto de httpx con 429/403.
            "User-Agent": "NAKED/2.0 (osint research tool)"
        }

        try:
            async with httpx.AsyncClient(
                timeout=10,
                headers=headers,
            ) as client:
                response = await client.get(url)
        except httpx.TimeoutException as e:
            raise ProviderUnavailableError(f"Reddit timeout: {e}") from e
        except httpx.RequestError as e:
            raise ProviderUnavailableError(f"Reddit network error: {e}") from e

        if response.status_code == 404:
            # Solo 404 significa "usuario no existe" de forma confiable.
            return None

        if response.status_code == 429:
            raise RateLimitError("Reddit rate limit exceeded (429)")

        if response.status_code == 403:
            # AMBIGUO a propósito: puede ser usuario suspendido/privado,
            # o el bloqueo del proxy/IP que ya vimos en el sandbox.
            # No podemos asumir "no existe" con esta info, así que es ERROR.
            raise ProviderUnavailableError(
                "Reddit returned 403 (suspended, private, or blocked — ambiguous)"
            )

        if response.status_code >= 500:
            raise ProviderUnavailableError(
                f"Reddit server error ({response.status_code})"
            )

        response.raise_for_status()

        payload = response.json()

        return payload.get("data")

    def _build_profile(self, data: dict[str, Any]) -> RedditProfile:
        """Convierte la respuesta de Reddit en un RedditProfile."""

        icon = data.get("icon_img", "")
        avatar_url = icon.split("?")[0] if icon else None

        return RedditProfile(
            display_name=data.get("subreddit", {}).get("title") or data.get("name"),
            avatar_url=avatar_url,
            bio=data.get("subreddit", {}).get("public_description") or None,
            karma_post=data.get("link_karma"),
            karma_comment=data.get("comment_karma"),
            is_verified=data.get("verified"),
            created_at=data.get("created_utc"),
        )

    def _build_result(
        self,
        username: str,
        data: dict[str, Any] | None,
    ) -> SearchResult:

        if data is None:
            return SearchResult(
                provider=self.name,
                username=username,
                exists=False,
                status=ResultStatus.NOT_FOUND,
                url=f"https://reddit.com/user/{username}",
            )

        profile = self._build_profile(data)

        result = SearchResult(
            provider=self.name,
            username=username,
            exists=True,
            status=ResultStatus.FOUND,
            url=f"https://reddit.com/user/{data.get('name', username)}",
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
            url=f"https://reddit.com/user/{username}",
        )
