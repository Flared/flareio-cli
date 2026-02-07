import datetime
import json
import pathlib
import pydantic
import typer

from flareio.api_client import FlareApiClient
from flareio_cli.api.client import get_api_client
from flareio_cli.api.models.events import EventItem
from flareio_cli.csv import PydanticCsvWriter
from flareio_cli.cursor import CursorFile
from flareio_cli.progress import export_progress

import typing as t


class CsvItem(pydantic.BaseModel):
    uid: str = pydantic.Field(serialization_alias="metadata.uid")
    matched_at: str = pydantic.Field(serialization_alias="metadata.matched_at")
    severity: str = pydantic.Field(serialization_alias="metadata.severity")
    notes: str | None = pydantic.Field(
        serialization_alias="tenant_metadata.notes", default=None
    )
    data: str = pydantic.Field(serialization_alias="data")


def _export(
    *,
    api_client: FlareApiClient,
    csv_writer: PydanticCsvWriter[CsvItem],
    cursor: CursorFile,
    filters: dict,
) -> None:
    with export_progress(
        object_name="events",
    ) as increment_progress:
        for event_item, event_data, next_cursor in api_client._scroll_events_items(
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
        ):
            cursor.save(next_cursor)

            event_item = EventItem.model_validate(event_item)

            csv_writer.writerow(
                row=CsvItem(
                    uid=event_item.metadata.uid,
                    matched_at=event_item.metadata.matched_at,
                    severity=event_item.metadata.severity,
                    notes=event_item.tenant_metadata.notes,
                    data=json.dumps(event_data),
                )
            )
            csv_writer.flush()

            increment_progress(
                incr_completed=1,
                new_cursor=next_cursor,
            )


def run_export_tenant_events(
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

    is_output_empty: bool = (
        not output_file.exists() or not output_file.read_text().strip()
    )

    # Run the export
    with open(output_file, "a+", encoding="utf-8") as f_output:
        csv_writer = PydanticCsvWriter(
            file=f_output,
            model=CsvItem,
        )
        if is_output_empty:
            csv_writer.writeheader()
        _export(
            api_client=api_client,
            csv_writer=csv_writer,
            cursor=cursor,
            filters=filters,
        )
