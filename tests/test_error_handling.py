from unittest.mock import AsyncMock, MagicMock, patch

import pytest

from naked.models.search_result import ResultStatus
from naked.providers.github.provider import GithubProvider
from naked.providers.reddit.provider import RedditProvider


def _mock_client(status_code: int, headers: dict | None = None, json_data: dict | None = None):
    response = MagicMock()
    response.status_code = status_code
    response.headers = headers or {}
    response.json.return_value = json_data or {"login": "x", "html_url": "https://github.com/x"}

    client = AsyncMock()
    client.get.return_value = response
    client.__aenter__.return_value = client
    client.__aexit__.return_value = False

    return client


@pytest.mark.asyncio
async def test_github_404_is_not_found():
    provider = GithubProvider()

    with patch("httpx.AsyncClient", return_value=_mock_client(404)):
        result = await provider.search("ghost")

    assert result.status == ResultStatus.NOT_FOUND
    assert result.exists is False
    assert result.error is None


@pytest.mark.asyncio
async def test_github_429_is_error_not_not_found():
    provider = GithubProvider()

    with patch("httpx.AsyncClient", return_value=_mock_client(429)):
        result = await provider.search("ghost")

    assert result.status == ResultStatus.ERROR
    assert result.exists is False
    assert result.error is not None


@pytest.mark.asyncio
async def test_github_403_with_rate_limit_header_is_rate_limit():
    provider = GithubProvider()
    client = _mock_client(403, headers={"X-RateLimit-Remaining": "0"})

    with patch("httpx.AsyncClient", return_value=client):
        result = await provider.search("ghost")

    assert result.status == ResultStatus.ERROR
    assert "rate limit" in result.error.lower()


@pytest.mark.asyncio
async def test_github_500_is_error():
    provider = GithubProvider()

    with patch("httpx.AsyncClient", return_value=_mock_client(500)):
        result = await provider.search("ghost")

    assert result.status == ResultStatus.ERROR


@pytest.mark.asyncio
async def test_reddit_403_is_error_not_not_found():
    """
    Caso real que vimos en el sandbox: Reddit responde 403 cuando
    bloquea la IP, no porque el usuario no exista. Esto NO debe
    aparecer como NOT_FOUND.
    """
    provider = RedditProvider()

    with patch("httpx.AsyncClient", return_value=_mock_client(403)):
        result = await provider.search("spez")

    assert result.status == ResultStatus.ERROR
    assert result.exists is False
    assert "ambiguous" in result.error.lower()


@pytest.mark.asyncio
async def test_reddit_404_is_not_found():
    provider = RedditProvider()

    with patch("httpx.AsyncClient", return_value=_mock_client(404)):
        result = await provider.search("definitely_does_not_exist_xyz")

    assert result.status == ResultStatus.NOT_FOUND
    assert result.error is None
