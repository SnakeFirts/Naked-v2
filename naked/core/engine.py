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
        logger.info("Searching '%s'...", username)

        session = self._create_session(username)

        start = time.perf_counter()

        results = await self._execute_providers(username)

        self._process_results(session, results)

        self._finish_session(session, start)

        return session

    def _create_session(self, username: str) -> SearchSession:
        return SearchSession(
            username=username,
            providers_loaded=len(self.providers),
        )

    async def _execute_providers(self, username: str):
        tasks = [
            provider.search(username)
            for provider in self.providers
        ]

        return await asyncio.gather(
            *tasks,
            return_exceptions=True,
        )

    def _process_results(
        self,
        session: SearchSession,
        results: list,
    ) -> None:

        for result in results:

            if isinstance(result, Exception):

                logger.exception(result)

                session.errors.append(str(result))

                continue

            session.results.append(result)

    def _finish_session(
        self,
        session: SearchSession,
        start: float,
    ) -> None:

        session.finished_at = datetime.utcnow()

        session.duration_ms = int(
            (time.perf_counter() - start) * 1000
        )

        logger.info(
            "Search completed in %d ms",
            session.duration_ms,
        )