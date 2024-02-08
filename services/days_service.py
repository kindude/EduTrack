import datetime
import uuid
from typing import List

from repositories.actions_repo import ActionsRepository
from repositories.days_repository import DaysRepository
from repositories.modules import ModulesRepository
from schemas.days.day import Day
from schemas.days.day_add_request import DayAddRequest
from schemas.days.day_module import DayModule
from schemas.users.user_marks import UserMarks


class DaysService:

    def __init__(self, days_repo: DaysRepository, actions_repo: ActionsRepository):

        self.days_repo = days_repo
        self.actions_repo = actions_repo

    async def add_day(self, day_add: DayAddRequest):

        day = Day(
            id=uuid.uuid4(),
            presence=day_add.presence,
            mark=day_add.mark,
            type_of_mark=day_add.type_of_mark,
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


    async def get_days_by_user(self, user_id: uuid.UUID) -> List[UserMarks]:
        days = await self.days_repo.get_days_by_user_id(user_id)
        if not days:
            return []
        return days

    async def get_days_users(self) -> List[UserMarks]:
        return await self.days_repo.get_days_users()

    async def get_days_by_teacher(self, teacher_id: uuid.UUID) -> List[UserMarks]:
        module_ids = await self.actions_repo.get_module_ids_by_teacher_id(teacher_id=teacher_id)
        print(module_ids)

        return await self.days_repo.get_days_by_teacher_id(module_ids=module_ids)

