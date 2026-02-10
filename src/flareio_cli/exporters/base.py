import dataclasses
import pathlib

import pydantic
import typer

import typing as t

from flareio_cli.csv import PydanticCsvWriter
from flareio_cli.cursor import CursorFile
from flareio_cli.progress import export_progress


ExportItem = t.TypeVar("ExportItem", bound=pydantic.BaseModel)


@dataclasses.dataclass(frozen=True)
class ExportPage(t.Generic[ExportItem]):
    items: list[ExportItem]
    next: str | None


def export_to_csv(
    *,
    output_file: pathlib.Path,
    pages: t.Iterator[ExportPage[ExportItem]],
    cursor: CursorFile,
    object_name: str = "items",
    item_model: type[ExportItem],
) -> None:
    try:
        _export_to_csv(
            output_file=output_file,
            pages=pages,
            cursor=cursor,
            object_name=object_name,
            item_model=item_model,
        )
    except KeyboardInterrupt:
        typer.echo(f"Stopping import. You may resume using cursor={cursor.value()}")
        raise typer.Abort()


def _export_to_csv(
    *,
    output_file: pathlib.Path,
    pages: t.Iterator[ExportPage[ExportItem]],
    cursor: CursorFile,
    object_name: str = "items",
    item_model: type[ExportItem],
) -> None:
    is_output_empty: bool = (
        not output_file.exists() or not output_file.read_text().strip()
    )

    with (
        open(output_file, "a+", encoding="utf-8") as f_output,
        export_progress(object_name=object_name) as progress_manager,
    ):
        writer = PydanticCsvWriter(
            file=f_output,
            model=item_model,
        )
        if is_output_empty:
            writer.writeheader()

        for page in pages:
            for row in page.items:
                writer.writerow(row)
                writer.flush()

            cursor.save(page.next)

            progress_manager.update_progress(
                incr_completed=len(page.items),
                new_cursor=cursor.value(),
            )
