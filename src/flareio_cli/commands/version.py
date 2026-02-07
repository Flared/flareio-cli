import typer

from flareio_cli.version import __version__


def run_version() -> None:
    typer.echo(f"flareio-cli {__version__}")
