import pydantic


class EventMetadata(pydantic.BaseModel):
    estimated_created_at: str
    matched_at: str
    uid: str
    severity: str


class EventTenantMetadata(pydantic.BaseModel):
    tags: list[str] = []
    notes: str | None = None


class EventItem(pydantic.BaseModel):
    metadata: EventMetadata
    tenant_metadata: EventTenantMetadata
