import asyncio

import typer

from naked.core.engine import NakedEngine
from naked.core.plugin_manager import PluginManager
from naked.core.display import render_session

app = typer.Typer()


async def _run(username: str) -> None:
    manager = PluginManager()
    providers = manager.load()
    engine = NakedEngine(providers)
    session = await engine.search(username)
    render_session(session)


@app.command()
def search(
    username: str = typer.Argument(..., help="Username to search across loaded providers."),
) -> None:
    """Search a username across all available providers."""
    asyncio.run(_run(username))


if __name__ == "__main__":
    app()
