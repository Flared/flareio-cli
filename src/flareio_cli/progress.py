import contextlib

from rich.progress import Progress
from rich.progress import SpinnerColumn
from rich.progress import TaskID
from rich.progress import TextColumn
from rich.progress import TimeElapsedColumn

import typing as t


class ExportProgressManager:
    def __init__(
        self,
        *,
        progress: Progress,
        task_id: TaskID,
    ) -> None:
        self.progress: Progress = progress
        self.task_id: TaskID = task_id

        self.current_completed: int = 0
        self.current_cursor: str | None = None

    def update_progress(
        self,
        *,
        incr_completed: int,
        new_cursor: str | None = None,
    ) -> None:
        self.current_completed = self.current_completed + incr_completed

        self.progress.update(
            self.task_id,
            completed=self.current_completed,
            cursor=new_cursor or self.current_cursor,
        )


@contextlib.contextmanager
def export_progress(
    *,
    object_name: str,
) -> t.Iterator[ExportProgressManager]:
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
        progress_manager = ExportProgressManager(
            progress=progress,
            task_id=progress.add_task(
                description=f"Exporting {object_name}...",
                total=None,
                cursor=None,
            ),
        )
        yield progress_manager
