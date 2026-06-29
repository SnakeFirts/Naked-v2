import asyncio

from naked.core.engine import NakedEngine
from naked.core.registry import Registry

from naked.providers.dummy.provider import DummyProvider

registry = Registry()

registry.register(DummyProvider())

engine = NakedEngine(registry)

asyncio.run(
    engine.search("snakefirts")
)