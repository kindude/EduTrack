import datetime
import uuid
from typing import List

from repositories.days_repository import DaysRepository
from schemas.days.day import Day
from schemas.days.day_add_request import DayAddRequest
from schemas.days.day_module import DayModule
from schemas.users.user_marks import UserMarks


class DaysService:

    def __init__(self, days_repo: DaysRepository):

        self.days_repo = days_repo

    async def add_day(self, day_add: DayAddRequest):

        day = Day(
            id=uuid.uuid4(),
            presence=day_add.presence,
            mark=day_add.mark,
            user_id=day_add.user_id,
            module_id=day_add.module_id,
            date=datetime.datetime.now()
        )

        await self.days_repo.add_day(day)

    async def get_days_by_module(self, module_id: uuid.UUID):
        days = await self.days_repo.get_days_by_module_id(module_id)
        if not days:
            return []
        else:
            pass


    async def get_days_by_user(self, user_id: uuid.UUID) -> List[DayModule]:
        days = await self.days_repo.get_days_by_user_id(user_id)
        if not days:
            return []
        return days

    async def get_days_users(self) -> List[UserMarks]:
        return await self.days_repo.get_days_users()

    def __to_DayInfo(self, day: Day):
        pass
