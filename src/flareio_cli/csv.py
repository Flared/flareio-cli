import csv

from pydantic import BaseModel

import typing as t

from flareio_cli.cursor import Cursor


CsvModel = t.TypeVar("CsvModel", bound=BaseModel)


class PydanticCsvWriter(t.Generic[CsvModel]):
    def __init__(
        self,
        *,
        file: t.TextIO,
        model: t.Type[CsvModel],
    ) -> None:
        fieldnames = [
            field_info.serialization_alias or field_name
            for field_name, field_info in model.model_fields.items()
        ]
        fieldnames.append("next")
        self.dict_writer = csv.DictWriter(
            file,
            fieldnames=fieldnames,
            lineterminator="\n",
        )
        self.file = file

    def writeheader(self) -> None:
        self.dict_writer.writeheader()

    def writerow(
        self,
        *,
        row: CsvModel,
        cursor: Cursor,
    ) -> None:
        dumped: dict = row.model_dump(by_alias=True)
        dumped["next"] = cursor.value()
        self.dict_writer.writerow(dumped)

    def flush(self) -> None:
        self.file.flush()
