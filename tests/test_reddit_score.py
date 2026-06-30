from naked.intelligence.score import ScoreCalculator
from naked.models.profiles.reddit import RedditProfile
from naked.models.search_result import SearchResult


def _reddit_result(exists: bool = True, verified: bool = False) -> SearchResult:
    profile = None
    if exists:
        profile = RedditProfile(
            display_name="spez",
            karma_post=1000,
            karma_comment=500,
            is_verified=verified,
        )

    return SearchResult(
        provider="reddit",
        username="spez",
        exists=exists,
        url="https://reddit.com/user/spez" if exists else None,
        profile=profile,
    )


def test_reddit_unverified_does_not_score_100():
    result = _reddit_result(verified=False)

    score = ScoreCalculator.calculate(result)

    assert score is not None
    assert score.score == 80
    assert "Verified account" not in score.reasons


def test_reddit_verified_scores_100():
    result = _reddit_result(verified=True)

    score = ScoreCalculator.calculate(result)

    assert score.score == 100
    assert "Verified account" in score.reasons


def test_reddit_nonexistent_has_no_score():
    result = _reddit_result(exists=False)

    score = ScoreCalculator.calculate(result)

    assert score is None
