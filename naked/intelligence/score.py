from naked.intelligence.rules import RULES_BY_PROVIDER
from naked.models.intelligence_score import IntelligenceScore
from naked.models.search_result import SearchResult

class ScoreCalculator:
    """
    Calcula un IntelligenceScore a partir de un SearchResult,
    usando las reglas registradas para ese provider.
    """

    MAX_SCORE = 100

    @classmethod
    def calculate(cls, result: SearchResult) -> IntelligenceScore | None:
        if not result.exists:
            return None

        rules_fn = RULES_BY_PROVIDER.get(result.provider)

        if rules_fn is None:
            # No hay reglas definidas todavía para este provider.
            return None

        applied = rules_fn(result)

        total = sum(evidence.points for evidence in applied if evidence.passed)
        total = max(0, min(total, cls.MAX_SCORE))

        reasons = [
            evidence.description
            for evidence in applied
            if evidence.passed
        ]

        return IntelligenceScore(
            score=total,
            reasons=reasons,
            evidences=applied,
        )
