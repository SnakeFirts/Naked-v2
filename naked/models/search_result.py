from enum import Enum
from typing import Any

from pydantic import BaseModel

from naked.models.profiles.base import BaseProfile
from naked.models.intelligence_score import IntelligenceScore


class ResultStatus(str, Enum):
    FOUND = "found"
    NOT_FOUND = "not_found"
    ERROR = "error"


class SearchResult(BaseModel):

    provider: str

    username: str

    exists: bool

    status: ResultStatus = ResultStatus.NOT_FOUND

    error: str | None = None

    url: str | None = None

    profile: BaseProfile | None = None

    raw: dict[str, Any] | None = None

    score: IntelligenceScore | None = None
