import asyncio

import typer

from naked.core.engine import NakedEngine
from naked.core.plugin_manager import PluginManager

app = typer.Typer()


async def _run(username: str) -> None:
    manager = PluginManager()

    providers = manager.load()

    engine = NakedEngine(providers)

    session = await engine.search(username)

    for result in session.results:
        print(result.model_dump())

    print()
    print(session.model_dump())


@app.command()
def search(
    username: str = typer.Argument(..., help="Username a buscar en los providers cargados."),
) -> None:
    """Busca un username en todos los providers disponibles."""

    asyncio.run(_run(username))


if __name__ == "__main__":
    app()