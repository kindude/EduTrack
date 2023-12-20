import datetime
from typing import Optional
from uuid import UUID

from schemas.base import BaseSchema


class Day(BaseSchema):
    id: UUID
    presence: bool
    mark: Optional[float] = None
    user_id: UUID
    module_id: UUID
    date: datetime.datetime
