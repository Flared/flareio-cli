import csv
import pathlib


class Cursor:
    def __init__(
        self,
        *,
        value: str | None,
    ) -> None:
        self._value: str | None = value

    def value(self) -> str | None:
        return self._value

    def save(self, value: str | None) -> None:
        if not value:
            return
        self._value = value

    @classmethod
    def from_csv(
        cls,
        *,
        path: pathlib.Path,
    ) -> "Cursor":
        cursor = cls(value=None)

        if not path.exists():
            return cursor

        with open(path, "r", encoding="utf-8") as f:
            csv_reader = csv.DictReader(f)
            for row in csv_reader:
                next_ = row.get("next")
                cursor.save(next_)

        return cursor
