import uuid
import datetime

from pydantic import constr

from schemas.base import BaseSchema
from schemas.modules.module_info import ModuleInfo
from schemas.users.user import UserInfo


class PostInfo(BaseSchema):
    id: uuid.UUID
    title: constr(min_length=2)
    text: constr(min_length=2)
    date: datetime.datetime
    author: UserInfo
    module: ModuleInfo
