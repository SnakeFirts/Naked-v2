from pydantic import BaseModel

class Profile(BaseModel):

    followers: int | None = None

    following: int | None = None

    posts: int | None = None

    bio: str | None = None

    verified: bool = False