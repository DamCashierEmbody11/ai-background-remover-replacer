"""Command-line entry point for the desktop host."""
from __future__ import annotations

import logging
from pathlib import Path
from typing import Optional

import typer
from rich.console import Console

from bgremover.core.host import PluginHost
from bgremover.core.pipeline import RemovalPipeline
from bgremover.config.settings import Settings

app = typer.Typer(help="AI background remover / replacer — plugin host.")
console = Console()


@app.command()
def run(
    image: Path = typer.Argument(..., exists=True, dir_okay=False),
    out: Optional[Path] = typer.Option(None, "--out", "-o"),
    background: Optional[Path] = typer.Option(None, "--background", "-b"),
    plugin: str = typer.Option("u2net", "--plugin", "-p"),
) -> None:
    """Remove background from IMAGE and optionally composite a new one."""
    settings = Settings.load()
    host = PluginHost(settings)
    host.discover()

    remover = host.get_remover(plugin)
    pipeline = RemovalPipeline(remover, settings)

    result = pipeline.run(image, background=background, out=out)
    console.print(f"[green]saved[/green] {result}")


@app.command("list-plugins")
def list_plugins() -> None:
    """List every discovered remover/replacer plugin."""
    host = PluginHost(Settings.load())
    host.discover()
    for name, meta in host.registry.items():
        console.print(f"{name:20s} v{meta.version:8s} {meta.kind:10s} {meta.description}")


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    app()