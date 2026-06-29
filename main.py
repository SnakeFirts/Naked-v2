import asyncio

from naked.core.engine import NakedEngine
from naked.core.plugin_manager import PluginManager

async def main():
    manager = PluginManager()

    providers = manager.load()

    engine = NakedEngine(providers)

    session = await engine.search("snakefirts")

    for result in session.results:
        print(result.model_dump())

    print()
    print(session.model_dump())


if __name__ == "__main__":
    asyncio.run(main())