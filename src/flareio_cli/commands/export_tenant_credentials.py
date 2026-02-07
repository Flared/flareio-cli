import csv
import pathlib
import pydantic
import typer

from datetime import timedelta
from flareio._ratelimit import _Limiter
from flareio.api_client import FlareApiClient
from flareio_cli.api.client import get_api_client
from flareio_cli.api.models.credentials import CredentialItem
from flareio_cli.progress import export_progress

import typing as t


class CsvItem(pydantic.BaseModel):
    id: int = pydantic.Field()
    identity_name: str = pydantic.Field()
    hash: str = pydantic.Field()
    source_id: str = pydantic.Field()


def _get_dict_writer(output_file: t.TextIO) -> csv.DictWriter:
    fieldnames: list[str] = []
    for field_name, field_info in CsvItem.model_fields.items():
        fieldnames.append(field_info.serialization_alias or field_name)
    return csv.DictWriter(output_file, fieldnames=list(fieldnames))


def _export(
    *,
    api_client: FlareApiClient,
    cursor_file: pathlib.Path,
    dict_writer: csv.DictWriter,
    f_output: t.TextIO,
    cursor: str | None,
) -> None:
    pages_limiter: _Limiter = _Limiter(
        tick_interval=timedelta(seconds=1),
    )

    with export_progress(
        things_done="credentials exported",
    ) as increment_progress:
        for response in api_client.scroll(
            method="POST",
            url="/firework/v2/me/feed/credentials",
            json={
                "from": cursor,
                "size": 10,
                "order_type": "asc",
            },
        ):
            pages_limiter.tick()
            resp_json = response.json()

            # Save cursor to file
            next_cursor = resp_json["next"]
            if next_cursor is not None:
                cursor_file.write_text(next_cursor)

            for item in resp_json["items"]:
                credential_item = CredentialItem.model_validate(item)

                dict_writer.writerow(
                    CsvItem(
                        identity_name=credential_item.identity_name,
                        hash=credential_item.hash,
                        id=credential_item.id,
                        source_id=credential_item.source_id,
                    ).model_dump(
                        by_alias=True,
                    )
                )
                f_output.flush()

                increment_progress(1)


def run_export_tenant_credentials(
    *,
    cursor_file: t.Annotated[
        pathlib.Path,
        typer.Option(),
    ],
    output_file: t.Annotated[
        pathlib.Path,
        typer.Option(),
    ],
    format: t.Literal["csv"] = "csv",
):
    # Setup API client
    api_client: FlareApiClient = get_api_client()

    # Load existing cursor if it exists.
    cursor: str | None = cursor_file.read_text() if cursor_file.exists() else None
    cursor = cursor or None
    typer.echo(f"Found existing cursor. Will resume from {cursor=}")

    is_output_empty: bool = (
        not output_file.exists() or not output_file.read_text().strip()
    )

    # Run the export
    with open(output_file, "w+", encoding="utf-8") as f_output:
        dict_writer = _get_dict_writer(f_output)
        if is_output_empty:
            dict_writer.writeheader()
        _export(
            api_client=api_client,
            dict_writer=dict_writer,
            cursor_file=cursor_file,
            f_output=f_output,
            cursor=cursor,
        )
