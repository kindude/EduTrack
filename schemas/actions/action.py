import uuid

from models.user import Roles
from schemas.base import BaseSchema


class Action(BaseSchema):
    id: uuid.UUID
    user_id: uuid.UUID
    module_id: uuid.UUID
    role: Roles
