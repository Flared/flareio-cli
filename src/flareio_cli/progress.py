import contextlib

from rich.progress import Progress
from rich.progress import SpinnerColumn
from rich.progress import TextColumn
from rich.progress import TimeElapsedColumn

import typing as t


class ExportProgressUpdate(t.Protocol):
    def __call__(
        self,
        *,
        incr_completed: int,
        new_cursor: str | None = None,
    ) -> None: ...


@contextlib.contextmanager
def export_progress(
    *,
    object_name: str,
) -> t.Iterator[ExportProgressUpdate]:
    """
    Standard rich progress indicators so that all exports look the same.
    """
    with Progress(
        SpinnerColumn(),
        TextColumn("[bold blue]{task.description}"),
        TextColumn("[green]{task.completed} " + object_name + " exported"),
        TimeElapsedColumn(),
        TextColumn("[grey70]cursor={task.fields[cursor]}"),
    ) as progress:
        current_completed: int = 0
        current_cursor: str | None = None

        def _incr_progress(
            *,
            incr_completed: int,
            new_cursor: str | None = None,
        ) -> None:
            nonlocal current_completed
            current_completed = current_completed + incr_completed

            nonlocal current_cursor
            current_cursor = new_cursor or current_cursor

            progress.update(
                progress_task,
                completed=current_completed,
                cursor=current_cursor,
            )

        progress_task = progress.add_task(
            description=f"Exporting {object_name}...",
            total=None,
            cursor=None,
        )

        yield _incr_progress
