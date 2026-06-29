from pydantic import BaseModel

class SearchResult(BaseModel):
    provider: str
    username: str
    exists: bool
    url: str | None = None