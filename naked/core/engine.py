import asyncio
import time
from datetime import datetime

from naked.core.logger import logger
from naked.core.plugin import Provider
from naked.models.search_session import SearchSession


class NakedEngine:

    def __init__(self, providers: list[Provider]):
        self.providers = providers

    async def search(self, username: str) -> SearchSession:

        session = SearchSession(
            username=username,
            providers_loaded=len(self.providers),
        )

        logger.info("Searching '%s'...", username)

        start = time.perf_counter()

        tasks = [
            provider.search(username)
            for provider in self.providers
        ]

        results = await asyncio.gather(
            *tasks,
            return_exceptions=True,
        )

        for result in results:

            if isinstance(result, Exception):

                logger.exception(result)

                session.errors.append(str(result))

                continue

            session.results.append(result)

        session.finished_at = datetime.utcnow()

        session.duration_ms = int(
            (time.perf_counter() - start) * 1000
        )

        logger.info(
            "Search completed in %d ms",
            session.duration_ms,
        )

        return session