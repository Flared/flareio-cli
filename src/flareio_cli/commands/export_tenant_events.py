import datetime
import pathlib
import typer

from flareio.api_client import FlareApiClient
from flareio.models import ScrollEventsResult
from flareio_cli.api.client import get_api_client
from flareio_cli.cursor import CursorFile
from flareio_cli.exporters.events import export_events

import typing as t


app = typer.Typer()


@app.command()
def export_tenant_events(
    *,
    cursor_file: t.Annotated[pathlib.Path, typer.Option()],
    from_date: t.Annotated[datetime.datetime | None, typer.Option()] = None,
    output_file: t.Annotated[pathlib.Path, typer.Option()],
    format: t.Literal["csv"] = "csv",
) -> None:
    # Setup API client
    api_client: FlareApiClient = get_api_client()

    # Load existing cursor if it exists.
    cursor: CursorFile = CursorFile(path=cursor_file)
    if cursor.value():
        typer.echo(f"Found existing cursor. Will resume from cursor={cursor.value()}")

    # Ensure the date has a timezone.
    if from_date and not from_date.tzinfo:
        from_date = from_date.replace(tzinfo=datetime.timezone.utc)

    # Create filters
    filters: dict = dict()
    if from_date:
        filters["estimated_created_at"] = {"gte": from_date.isoformat()}

    events_iterator: t.Iterator[ScrollEventsResult] = api_client.scroll_events(
        method="POST",
        pages_url="/firework/v4/events/tenant/_search",
        events_url="/firework/v2/activities/",
        json={
            "size": 10,
            "order": "asc",
            "from": cursor.value(),
            "filters": filters,
            "query": {
                "type": "query_string",
                "query_string": "*",
            },
        },
    )

    export_events(
        output_file=output_file,
        events_iterator=events_iterator,
        cursor=cursor,
    )
