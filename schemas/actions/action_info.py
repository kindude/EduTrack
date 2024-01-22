import uuid

from models.user import Roles
from schemas.base import BaseSchema
from schemas.modules import ModuleInfo
from schemas.users.user import UserInfo


class ActionInfo(BaseSchema):
    id: uuid.UUID
    user: UserInfo
    module: ModuleInfo
    role: Roles
