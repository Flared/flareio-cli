import json
import pathlib
import pydantic

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


def export_events(
    *,
    output_file: pathlib.Path,
    events_iterator: t.Iterator[tuple[dict, dict, str | None]],
    cursor: CursorFile,
) -> None:
    is_output_empty: bool = (
        not output_file.exists() or not output_file.read_text().strip()
    )

    with (
        open(output_file, "a+", encoding="utf-8") as f_output,
        export_progress(object_name="events") as increment_progress,
    ):
        csv_writer = PydanticCsvWriter(
            file=f_output,
            model=CsvItem,
        )
        if is_output_empty:
            csv_writer.writeheader()

        for event_item, event_data, next_cursor in events_iterator:
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
