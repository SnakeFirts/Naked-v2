from pydantic import BaseModel

class Account(BaseModel):
    platform: str
    username: str
    exists: bool
    url: str | None = None