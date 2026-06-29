from datetime import datetime

from pydantic import BaseModel, Field

from naked.models.search_result import SearchResult

class SearchSession(BaseModel):
    username: str
    started_at: datetime = Field(default_factory=datetime.utcnow)
    finished_at: datetime | None = None
    duration_ms: int | None = None
    providers_loaded: int = 0
    results: list[SearchResult] = Field(default_factory=list)
    errors: list[str] = Field(default_factory=list)