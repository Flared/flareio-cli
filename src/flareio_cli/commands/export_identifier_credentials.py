import pathlib
import typer

from flareio.api_client import FlareApiClient
from flareio_cli.api.client import get_api_client
from flareio_cli.cursor import CursorFile
from flareio_cli.exporters.credentials import export_credentials

import typing as t


def run_export_identifier_credentials(
    *,
    cursor_file: t.Annotated[pathlib.Path, typer.Option()],
    output_file: t.Annotated[pathlib.Path, typer.Option()],
    identifier_id: t.Annotated[int, typer.Option()],
    format: t.Literal["csv"] = "csv",
) -> None:
    # Setup API client
    api_client: FlareApiClient = get_api_client()

    # Load existing cursor if it exists.
    cursor: CursorFile = CursorFile(path=cursor_file)
    if cursor.value():
        typer.echo(f"Found existing cursor. Will resume from cursor={cursor.value()}")

    # Run the export
    export_credentials(
        endpoint=f"/firework/v3/identifiers/{identifier_id}/feed/credentials",
        api_client=api_client,
        cursor=cursor,
        output_file=output_file,
    )
