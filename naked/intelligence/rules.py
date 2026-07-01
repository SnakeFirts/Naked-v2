from naked.models.intelligence_score import ScoreEvidence
from naked.models.search_result import SearchResult


def github_rules(result: SearchResult) -> list[ScoreEvidence]:
    rules: list[ScoreEvidence] = []

    rules.append(
        ScoreEvidence(
            name="official_api",
            description="Official GitHub API",
            points=40,
        )
    )

    if result.username and result.profile:
        rules.append(
            ScoreEvidence(
                name="username_match",
                description="Username exact match",
                points=20,
            )
        )

    if result.profile is not None:
        rules.append(
            ScoreEvidence(
                name="public_profile",
                description="Public profile",
                points=20,
            )
        )

    if result.url:
        rules.append(
            ScoreEvidence(
                name="profile_url",
                description="Profile URL verified",
                points=20,
            )
        )

    return rules


RULES_BY_PROVIDER = {
    "github": github_rules,
}
