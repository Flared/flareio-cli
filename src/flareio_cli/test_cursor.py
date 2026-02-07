import pathlib
import tempfile

from flareio_cli.cursor import CursorFile


def test_cursor_file() -> None:
    with tempfile.NamedTemporaryFile() as f:
        cursor_path = pathlib.Path(f.name)
        cursor = CursorFile(path=cursor_path)

        assert cursor.value() is None

        cursor.save("123")
        assert cursor.value() == "123"

        cursor.save(None)
        assert cursor.value() == "123"
