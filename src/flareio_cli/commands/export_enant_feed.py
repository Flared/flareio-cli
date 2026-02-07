import datetime
import flareio
import json
import pathlib
import typer

from flareio.api_client import FlareApiClient
from rich.progress import Progress
from rich.progress import SpinnerColumn

import typing as t


def _get_api_client() -> flareio.FlareApiClient:
    return flareio.FlareApiClient.from_env()


def run_export_tenant_feed(
    *,
    cursor_file: t.Annotated[
        pathlib.Path,
        typer.Option(),
    ],
    from_date: t.Annotated[
        datetime.datetime | None,
        typer.Option(),
    ] = None,
    output_file: t.Annotated[
        pathlib.Path,
        typer.Option(),
    ],
):
    # Setup API client
    api_client: FlareApiClient = _get_api_client()

    # Load existing cursor if it exists.
    cursor: str | None = cursor_file.read_text() if cursor_file.exists() else None
    cursor = cursor or None
    typer.echo(f"Found existing cursor. Will resume from {cursor=}")

    # Ensure the date has a timezone.
    if from_date and not from_date.tzinfo:
        from_date = from_date.replace(tzinfo=datetime.timezone.utc)

    # Create filters
    filters: dict = dict()
    if from_date:
        filters["estimated_created_at"] = {"gte": from_date.isoformat()}

    total_events: int = 0

    with open(output_file, "w+", encoding="utf-8") as f_output:
        with Progress(
            SpinnerColumn(),
        ) as progress:
            progress.add_task("Processing events", total=None)

            for event, next_cursor in api_client.scroll_events(
                method="POST",
                pages_url="/firework/v4/events/tenant/_search",
                events_url="/firework/v2/activities/",
                json={
                    "size": 10,
                    "order": "asc",
                    "from": cursor,
                    "filters": filters,
                    "query": {
                        "type": "query_string",
                        "query_string": "*",
                    },
                },
            ):
                # Save cursor to file
                if next_cursor is not None:
                    cursor_file.write_text(next_cursor)

                # Add event to the file
                f_output.write(json.dumps(event))

                # Print some status...
                total_events = total_events + 1
                if total_events % 20 == 0:
                    typer.echo(f" Processed {total_events} events...")
