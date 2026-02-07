import pathlib
import pydantic

from datetime import timedelta
from flareio._ratelimit import _Limiter
from flareio.api_client import FlareApiClient
from flareio_cli.api.models.credentials import CredentialItem
from flareio_cli.csv import PydanticCsvWriter
from flareio_cli.cursor import CursorFile
from flareio_cli.progress import export_progress


class CsvItem(pydantic.BaseModel):
    id: int = pydantic.Field()
    identity_name: str = pydantic.Field()
    hash: str = pydantic.Field()
    source_id: str = pydantic.Field()


def export_credentials(
    *,
    output_file: pathlib.Path,
    endpoint: str,
    api_client: FlareApiClient,
    cursor: CursorFile,
) -> None:
    pages_limiter: _Limiter = _Limiter(
        tick_interval=timedelta(seconds=1),
    )
    is_output_empty: bool = (
        not output_file.exists() or not output_file.read_text().strip()
    )

    with (
        open(output_file, "a+", encoding="utf-8") as f_output,
        export_progress(object_name="credentials") as increment_progress,
    ):
        csv_writer = PydanticCsvWriter(
            file=f_output,
            model=CsvItem,
        )
        if is_output_empty:
            csv_writer.writeheader()

        for response in api_client.scroll(
            method="POST",
            url=endpoint,
            json={
                "from": cursor.value(),
                "size": 10,
                "order_type": "asc",
            },
        ):
            pages_limiter.tick()
            resp_json = response.json()

            cursor.save(resp_json["next"])

            for item in resp_json["items"]:
                credential_item = CredentialItem.model_validate(item)

                csv_writer.writerow(
                    row=CsvItem(
                        identity_name=credential_item.identity_name,
                        hash=credential_item.hash,
                        id=credential_item.id,
                        source_id=credential_item.source_id,
                    ),
                )
                csv_writer.flush()

                increment_progress(
                    incr_completed=1,
                    new_cursor=cursor.value(),
                )
