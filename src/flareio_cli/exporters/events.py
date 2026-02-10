import json
import pathlib

import pydantic

import typing as t

from flareio.models import ScrollEventsResult

from flareio_cli.api.models.events import EventItem
from flareio_cli.cursor import CursorFile
from flareio_cli.exporters.base import ExportPage
from flareio_cli.exporters.base import export_to_csv


class EventExportItem(pydantic.BaseModel):
    uid: str = pydantic.Field(serialization_alias="metadata.uid")
    matched_at: str = pydantic.Field(serialization_alias="metadata.matched_at")
    severity: str = pydantic.Field(serialization_alias="metadata.severity")
    notes: str | None = pydantic.Field(
        serialization_alias="tenant_metadata.notes", default=None
    )
    data: str = pydantic.Field(serialization_alias="data")


def _event_pages(
    events_iterator: t.Iterator[ScrollEventsResult],
) -> t.Iterator[ExportPage[EventExportItem]]:
    for result in events_iterator:
        event_item = EventItem.model_validate(result.metadata)
        export_item = EventExportItem(
            uid=event_item.metadata.uid,
            matched_at=event_item.metadata.matched_at,
            severity=event_item.metadata.severity,
            notes=event_item.tenant_metadata.notes,
            data=json.dumps(result.event),
        )
        yield ExportPage(
            items=[export_item],
            next=result.next,
        )


def export_events(
    *,
    output_file: pathlib.Path,
    events_iterator: t.Iterator[ScrollEventsResult],
    cursor: CursorFile,
) -> None:
    export_to_csv(
        output_file=output_file,
        pages=_event_pages(
            events_iterator=events_iterator,
        ),
        cursor=cursor,
        object_name="events",
        item_model=EventExportItem,
    )
