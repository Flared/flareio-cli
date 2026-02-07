import pydantic


class CredentialItem(pydantic.BaseModel):
    hash: str
    id: int
    identity_name: str
    source_id: str
