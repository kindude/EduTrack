import uuid
from typing import List

from pydantic import BaseModel, constr

from schemas.base import BaseSchema


class ModuleInfo(BaseSchema):
    title: constr(min_length=5, max_length=100)
    hours_taught: int
    alias: constr(min_length=2, max_length=20)

    class Config:

        arbitrary_types_allowed = True
        from_attributes = True


class ModuleUpdateRequest(ModuleInfo):

    class Config:

        arbitrary_types_allowed = True
        from_attributes = True


class Module(ModuleInfo):
    id: uuid

    class Config:

        arbitrary_types_allowed = True
        from_attributes = True


class ModuleListResponse(BaseModel):
    Modules: List[ModuleInfo]

    class Config:

        arbitrary_types_allowed = True
        from_attributes = True


class ModuleException(Exception):
    pass


class ModuleNotFoundException(ModuleException):
    pass


class ModulesNotFoundException(ModuleException):
    pass


class ModuleExistsException(ModuleException):
    pass
