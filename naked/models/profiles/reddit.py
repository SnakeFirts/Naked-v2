from naked.models.profiles.base import BaseProfile


class RedditProfile(BaseProfile):

    karma_post: int | None = None

    karma_comment: int | None = None

    is_verified: bool | None = None

    created_at: int | None = None
