import tempfile

from pathlib import Path

from flareio_cli.cursor import Cursor


def test_cursor() -> None:
    cursor = Cursor(value=None)

    assert cursor.value() is None

    cursor.save("123")
    assert cursor.value() == "123"

    cursor.save(None)
    assert cursor.value() == "123"


def test_cursor_from_csv() -> None:
    with tempfile.NamedTemporaryFile() as f:
        f.write(
            """name,next
bob,first
bob,second
bob,
bob,third
bob,
""".encode()
        )
        f.flush()
        cursor = Cursor.from_csv(
            path=Path(f.name),
        )
        assert cursor.value() == "third"


def test_cursor_from_csv_none() -> None:
    with tempfile.NamedTemporaryFile() as f:
        f.write(
            """name,next
bob,
""".encode()
        )
        f.flush()
        cursor = Cursor.from_csv(
            path=Path(f.name),
        )
        assert cursor.value() is None
