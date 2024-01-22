import uuid

from schemas.base import BaseSchema


class Module(BaseSchema):
    id: uuid.UUID
    title: str
    alias: str
    hours_taught: int
