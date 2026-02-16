import io

import pydantic

from flareio_cli.csv import PydanticCsvWriter
from flareio_cli.cursor import Cursor


def test_pydantic_csv_writer() -> None:
    csv_file_str = io.StringIO()

    class TestModel(pydantic.BaseModel):
        first_field: int
        second_field: str = pydantic.Field(serialization_alias="second.field")

    writer = PydanticCsvWriter(
        file=csv_file_str,
        model=TestModel,
    )

    writer.writeheader()
    writer.writerow(
        row=TestModel(first_field=1, second_field="Alice"),
        cursor=Cursor(value=None),
    )
    writer.writerow(
        row=TestModel(first_field=2, second_field="Bob"),
        cursor=Cursor(value=None),
    )

    assert (
        csv_file_str.getvalue()
        == """first_field,second.field,next
1,Alice,
2,Bob,
"""
    )
