from datetime import datetime
from typing import Optional
from uuid import UUID

from schemas.base import BaseSchema
from schemas.modules import ModuleInfo
from schemas.user import UserInfo


class DayInfo(BaseSchema):
    id: UUID
    presence: bool
    mark: Optional[float] = None
    user: UserInfo
    module: ModuleInfo
    date: datetime
