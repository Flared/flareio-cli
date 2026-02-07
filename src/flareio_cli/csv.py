import csv

from pydantic import BaseModel

import typing as t


CsvModel = t.TypeVar("CsvModel", bound=BaseModel)


class PydanticCsvWriter(t.Generic[CsvModel]):
    def __init__(
        self,
        *,
        file: t.TextIO,
        model: t.Type[CsvModel],
    ) -> None:
        self.dict_writer = csv.DictWriter(
            file,
            fieldnames=[
                field_info.serialization_alias or field_name
                for field_name, field_info in model.model_fields.items()
            ],
            lineterminator="\n",
        )
        self.file = file

    def writeheader(self) -> None:
        self.dict_writer.writeheader()

    def writerow(self, row: CsvModel) -> None:
        dumped = row.model_dump(by_alias=True)
        self.dict_writer.writerow(dumped)

    def flush(self) -> None:
        self.file.flush()
