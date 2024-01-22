from typing import List, Iterable
from uuid import UUID

from sqlalchemy import select
from sqlalchemy.orm import selectinload

from models.day import DayDao
from repositories.base import BaseRepository
from schemas.days.day import Day
from schemas.days.day_info import DayInfo
from schemas.days.day_module import DayModule
from schemas.modules.module_info import ModuleInfo
from schemas.users.user_marks import UserMarks


class DaysRepository(BaseRepository):

    model = DayDao

    async def add_day(self, day: Day):
        await self._add(day.model_dump())

    async def get_days_by_module_id(self, module_id: UUID) -> List[Day]:
        stmt_to_select_days = select(DayDao).filter(DayDao.module_id == module_id).options(
            selectinload(DayDao.module),
            selectinload(DayDao.user)
        )
        days = await self.session.execute(stmt_to_select_days)
        days = days.scalars().all()
        print(days[0].presence, days[0].module.title)
        return []

    async def get_days_by_user_id(self, user_id: UUID) -> List[DayModule]:
        stmt_to_select_days = select(DayDao).filter(DayDao.user_id == user_id).options(
            selectinload(DayDao.module),
        )
        days = await self.session.execute(stmt_to_select_days)
        days = days.scalars().all()
        days_module = []
        for day in days:
            d = DayInfo.model_validate(day)
            module = ModuleInfo.model_validate(day.module)
            days_module.append(DayModule(
                day=d,
                module=module
            ))

        return days_module

    async def get_days_by_module_user(self, user_id: UUID, module_id: UUID) -> List[DayInfo]:
        stmt_to_select_days = select(DayDao).filter((DayDao.user_id == user_id) and (DayDao.module_id == module_id))
        days = await self.session.execute(stmt_to_select_days)
        return [DayInfo.model_validate(day) for day in days]

    async def get_days_users(self) -> List[UserMarks]:
        stmt_to_select_days = select(DayDao).options(
            selectinload(DayDao.module),
            selectinload(DayDao.user)
        )
        days = await self.session.execute(stmt_to_select_days)

        grouped_days = {}
        for day in days.scalars().all():
            user_id = day.user.id
            module_title = day.module.title

            if (user_id, module_title) not in grouped_days:
                grouped_days[(user_id, module_title)] = []

            grouped_days[(user_id, module_title)].append(day)

        users_marks = [
            UserMarks(
                id=user_id,
                first_name=grouped_days[key][0].user.first_name,
                last_name=grouped_days[key][0].user.last_name,
                module_title=module_title,
                days=[DayInfo.model_validate(day) for day in grouped_days[key]]
            )
            for key, days in grouped_days.items()
        ]

        return users_marks


    def __to_User_Marks(self, days: Iterable[DayDao]) -> List[UserMarks]:

        users_marks = []

        for day in days:

            users_marks.append(UserMarks(
                id=day.user.id,
                first_name=day.user.first_name,
                last_name=day.user.last_name,
                module_title=day.module.title,
                days=[DayInfo.model_validate(day)]
            ))

        return users_marks
