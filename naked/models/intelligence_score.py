from pydantic import BaseModel


class ScoreEvidence(BaseModel):
    name: str
    description: str
    points: int
    passed: bool = True


class IntelligenceScore(BaseModel):
    score: int
    reasons: list[str]
    evidences: list[ScoreEvidence]
    
