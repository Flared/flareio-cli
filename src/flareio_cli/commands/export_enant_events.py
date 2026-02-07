import csv
import datetime
import json
import pathlib
import pydantic
import typer

from flareio.api_client import FlareApiClient
from flareio_cli.api.client import get_api_client
from flareio_cli.api.models.events import EventItem
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


def _get_dict_writer(output_file: t.TextIO) -> csv.DictWriter:
    fieldnames: set[str] = set()

    for field_name, field_info in CsvItem.model_fields.items():
        fieldnames.add(field_info.serialization_alias or field_name)

    return csv.DictWriter(output_file, fieldnames=list(fieldnames))


def _export(
    *,
    api_client: FlareApiClient,
    cursor_file: pathlib.Path,
    dict_writer: csv.DictWriter,
    f_output: t.TextIO,
    cursor: str | None,
    filters: dict,
) -> None:
    with export_progress(
        things_done="events exported",
    ) as increment_progress:
        for event_item, event_data, next_cursor in api_client._scroll_events_items(
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

            event_item = EventItem.model_validate(event_item)

            dict_writer.writerow(
                CsvItem(
                    uid=event_item.metadata.uid,
                    matched_at=event_item.metadata.matched_at,
                    severity=event_item.metadata.severity,
                    notes=event_item.tenant_metadata.notes,
                    data=json.dumps(event_data),
                ).model_dump(
                    by_alias=True,
                )
            )
            f_output.flush()

            increment_progress()


def run_export_tenant_events(
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
    format: t.Literal["csv"] = "csv",
):
    # Setup API client
    api_client: FlareApiClient = get_api_client()

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

    is_output_empty: bool = (
        not output_file.exists() or not output_file.read_text().strip()
    )

    # Run the export
    with open(output_file, "w+", encoding="utf-8") as f_output:
        dict_writer = _get_dict_writer(f_output)
        if is_output_empty:
            dict_writer.writeheader()
        _export(
            api_client=api_client,
            dict_writer=dict_writer,
            cursor_file=cursor_file,
            f_output=f_output,
            cursor=cursor,
            filters=filters,
        )
