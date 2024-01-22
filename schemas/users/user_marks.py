import uuid
from typing import List

from schemas.base import BaseSchema
from schemas.days.day_info import DayInfo


class UserMarks(BaseSchema):
    id: uuid.UUID
    first_name: str
    last_name: str
    module_title: str
    days: List[DayInfo]
