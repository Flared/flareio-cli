import pathlib

from datetime import timedelta

import pydantic
import requests

import typing as t

from flareio.ratelimit import Limiter

from flareio_cli.api.models.credentials import CredentialItem
from flareio_cli.cursor import CursorFile
from flareio_cli.exporters.base import ExportPage
from flareio_cli.exporters.base import export_to_csv


class CredentialExportItem(pydantic.BaseModel):
    id: int = pydantic.Field()
    identity_name: str = pydantic.Field()
    hash: str = pydantic.Field()
    source_id: str = pydantic.Field()

    @classmethod
    def from_credential_item(cls, *, item: CredentialItem) -> "CredentialExportItem":
        return cls(
            id=item.id,
            identity_name=item.identity_name,
            hash=item.hash,
            source_id=item.source_id,
        )


def _credentials_pages(
    *,
    resp_iterator: t.Iterator[requests.Response],
) -> t.Iterator[ExportPage[CredentialExportItem]]:
    pages_limiter = Limiter(tick_interval=timedelta(seconds=1))

    for response in resp_iterator:
        pages_limiter.tick()

        resp_json = response.json()

        next: str | None = resp_json["next"]
        items = [
            CredentialExportItem.from_credential_item(
                item=CredentialItem.model_validate(item),
            )
            for item in resp_json["items"]
        ]

        yield ExportPage(
            items=items,
            next=next,
        )


def export_credentials(
    *,
    output_file: pathlib.Path,
    resp_iterator: t.Iterator[requests.Response],
    cursor: CursorFile,
) -> None:
    export_to_csv(
        output_file=output_file,
        pages=_credentials_pages(
            resp_iterator=resp_iterator,
        ),
        cursor=cursor,
        object_name="credentials",
        item_model=CredentialExportItem,
    )
