import uuid

from models.user import Roles
from schemas.base import BaseSchema


class ActionAddRequest(BaseSchema):
    user_id: uuid.UUID
    module_id: uuid.UUID
    role: Roles
