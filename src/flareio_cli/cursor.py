import pathlib


class CursorFile:
    def __init__(
        self,
        *,
        path: pathlib.Path,
    ) -> None:
        self._path = path
        self._cached_value: str | None = None

    def value(self) -> str | None:
        if self._cached_value:
            return self._cached_value
        if not self._path.exists():
            return None
        cursor = self._path.read_text().strip() or None
        self._cached_value = cursor
        return cursor

    def save(self, value: str | None) -> None:
        if not value:
            return
        self._cached_value = value
        self._path.write_text(value)
