import contextlib

from rich.progress import Progress
from rich.progress import SpinnerColumn
from rich.progress import TextColumn
from rich.progress import TimeElapsedColumn

import typing as t


@contextlib.contextmanager
def export_progress(
    things_done: str,
) -> t.Iterator[t.Callable[[int], None],]:
    """
    Standard rich progress indicators so that all exports look the same.
    """
    with Progress(
        SpinnerColumn(),
        TextColumn("[bold blue]{task.description}"),
        TextColumn("[green]{task.completed} " + things_done),
        TimeElapsedColumn(),
    ) as progress:
        total_completed = 0

        def _incr_progress(
            completed: int = 1,
        ) -> None:
            nonlocal total_completed
            total_completed = total_completed + completed
            progress.update(
                progress_task,
                completed=total_completed,
            )

        progress_task = progress.add_task("Exporting events...", total=None)

        yield _incr_progress
