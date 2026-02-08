import typer

from flareio_cli.version import __version__


app = typer.Typer()


@app.command()
def version() -> None:
    typer.echo(f"flareio-cli {__version__}")
