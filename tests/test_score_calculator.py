from naked.intelligence.score import ScoreCalculator
from naked.models.profiles.github import GithubProfile
from naked.models.search_result import SearchResult


def _github_result(exists: bool = True, with_profile: bool = True) -> SearchResult:
    profile = None
    if with_profile:
        profile = GithubProfile(
            display_name="Snake",
            followers=10,
            following=5,
            repositories=20,
        )

    return SearchResult(
        provider="github",
        username="snakefirts",
        exists=exists,
        url="https://github.com/snakefirts" if exists else None,
        profile=profile,
    )


def test_github_full_match_scores_100():
    result = _github_result()

    score = ScoreCalculator.calculate(result)

    assert score is not None
    assert score.score == 100
    assert "Official API" in score.reasons


def test_nonexistent_profile_has_no_score():
    result = _github_result(exists=False, with_profile=False)

    score = ScoreCalculator.calculate(result)

    assert score is None


def test_unknown_provider_has_no_score():
    result = SearchResult(
        provider="tiktok",
        username="snakefirts",
        exists=True,
    )

    score = ScoreCalculator.calculate(result)

    assert score is None


def test_score_never_exceeds_max():
    result = _github_result()

    score = ScoreCalculator.calculate(result)

    assert score.score <= ScoreCalculator.MAX_SCORE
