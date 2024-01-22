import uuid

from schemas.base import BaseSchema


class ModuleInfo(BaseSchema):
    id: uuid.UUID
    title: str
    alias: str
    hours_taught: int
