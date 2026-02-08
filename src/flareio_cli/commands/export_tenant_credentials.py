import pathlib
import typer

from flareio.api_client import FlareApiClient
from flareio_cli.api.client import get_api_client
from flareio_cli.cursor import CursorFile
from flareio_cli.exporters.credentials import export_credentials

import typing as t


app = typer.Typer()


@app.command()
def export_tenant_credentials(
    *,
    cursor_file: t.Annotated[pathlib.Path, typer.Option()],
    output_file: t.Annotated[pathlib.Path, typer.Option()],
    format: t.Literal["csv"] = "csv",
) -> None:
    # Setup API client
    api_client: FlareApiClient = get_api_client()

    # Load existing cursor if it exists.
    cursor: CursorFile = CursorFile(path=cursor_file)
    if cursor.value():
        typer.echo(f"Found existing cursor. Will resume from cursor={cursor.value()}")

    # Configure scrolling
    resp_iterator = api_client.scroll(
        url="firework/v2/me/feed/credentials",
        method="GET",
        params={
            "from": cursor.value(),
            "limit": 100,
        },
    )

    # Run the export
    export_credentials(
        resp_iterator=resp_iterator,
        cursor=cursor,
        output_file=output_file,
    )
