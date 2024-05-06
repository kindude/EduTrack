import datetime
from typing import Optional
from uuid import UUID

from models.attendance import AttendanceTypes
from models.type_of_mark import MarkTypes
from schemas.base import BaseSchema


class DayAddRequest(BaseSchema):
    presence: AttendanceTypes
    type_of_mark: MarkTypes
    mark: Optional[float] = None
    user_id: UUID
    module_id: UUID
    date: str
