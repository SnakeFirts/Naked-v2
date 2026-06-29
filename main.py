import asyncio

from naked.core.engine import NakedEngine
from naked.core.registry import Registry

from naked.providers.dummy.provider import DummyProvider

async def main():
    registry = Registry()
    registry.register(DummyProvider())
    engine = NakedEngine(registry)
    results = await engine.search("snakefirts")
    print(results)

asyncio.run(main())