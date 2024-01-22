from schemas.base import BaseSchema


class ModuleAddRequest(BaseSchema):

    title: str
    hours_taught: int
    alias: str
