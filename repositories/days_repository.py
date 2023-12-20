from typing import List
from uuid import UUID

from sqlalchemy import select
from sqlalchemy.orm import selectinload

from models.day import DayDao
from repositories.base import BaseRepository
from schemas.days.day import Day


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

    async def get_days_by_user_id(self, user_id: UUID) -> List[Day]:
        stmt_to_select_days = select(DayDao).filter(DayDao.user_id == user_id).options(
            selectinload(DayDao.module),
            selectinload(DayDao.user)
        )
        days = await self.session.execute(stmt_to_select_days)
        days = days.scalars().all()
        print(days[0].presence, days[0].user.first_name)
        return []