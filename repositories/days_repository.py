import uuid
from typing import List, Iterable
from uuid import UUID

from sqlalchemy import select, any_, or_
from sqlalchemy.orm import selectinload, contains_eager
from sqlalchemy.sql.selectable import and_

from models.attendance import AttendanceDao
from models.day import DayDao
from models.type_of_mark import TypeOfMarkDao
from models.user import UserDao
from repositories.base import BaseRepository
from schemas.days.day import Day
from schemas.days.day_info import DayInfo
from schemas.days.day_module import DayModule
from schemas.modules.module_info import ModuleInfo
from schemas.users.user_marks import UserMarks


class DaysRepository(BaseRepository):

    model = DayDao

    async def add_day(self, day: Day):
        try:
            stmt_to_select_type_of_mark = select(TypeOfMarkDao).filter(TypeOfMarkDao.type_of_mark == day.type_of_mark)
            type_of_mark = await self.session.execute(stmt_to_select_type_of_mark)
            type_of_mark = type_of_mark.scalar_one_or_none()

            stmt_to_select_type_of_attendance = select(AttendanceDao).filter(AttendanceDao.type == day.presence)
            type_of_attendance = await self.session.execute(stmt_to_select_type_of_attendance)
            type_of_attendance = type_of_attendance.scalar_one_or_none()

            day_dump = day.model_dump()
            del day_dump["presence"]
            del day_dump["type_of_mark"]
            day_dump["presence_id"] = type_of_attendance.id
            day_dump["type_of_mark_id"] = type_of_mark.id
            await self._add(day_dump)
        except Exception as exc:
            print(exc)

    async def get_days_by_module_id(self, module_id: UUID) -> List[Day]:
        stmt_to_select_days = select(DayDao).filter(DayDao.module_id == module_id).options(
            selectinload(DayDao.module),
            selectinload(DayDao.user)
        )
        days = await self.session.execute(stmt_to_select_days)
        days = days.scalars().all()
        return []

    async def get_days_by_user_id(self, user_id: UUID) -> List[UserMarks]:

        stmt_to_select_user = select(UserDao).filter(UserDao.id == user_id).options(selectinload(UserDao.days).options(selectinload(DayDao.module),
                                                                                          selectinload(
                                                                                              DayDao.type_of_mark),
                                                                                          selectinload(
                                                                                              DayDao.presence)))

        user_days = await self.session.execute(stmt_to_select_user)

        user_days = user_days.scalars().all()
        user_marks = self.__to_User_Marks(user_days)
        return user_marks


    async def get_days_by_module_user(self, user_id: UUID, module_id: UUID) -> List[DayInfo]:
        stmt_to_select_days = select(DayDao).filter((DayDao.user_id == user_id) and (DayDao.module_id == module_id))
        days = await self.session.execute(stmt_to_select_days)
        days = days.scalars().all()
        return [self.__to_DayInfo(day) for day in days]

    async def get_days_users(self) -> List[UserMarks]:
        stmt_to_select_users = select(UserDao).options(selectinload(UserDao.days).options( selectinload(DayDao.module),
            selectinload(DayDao.type_of_mark),
            selectinload(DayDao.presence)))

        users_days = await self.session.execute(stmt_to_select_users)

        users_days = users_days.scalars().all()
        users_marks = self.__to_User_Marks(users_days)

        return users_marks

    async def get_days_by_teacher_id(self, module_ids: List[uuid.UUID]) -> List[UserMarks]:
        # Define the subquery to filter days based on module_ids
        subquery = (
            select(UserDao)
            .options(
                selectinload(UserDao.days)  # Ensure UserDao.days is eagerly loaded
                .options(
                    selectinload(DayDao.module),
                    selectinload(DayDao.type_of_mark),
                    selectinload(DayDao.presence)
                )
            )
        )

        # Execute the subquery to retrieve the filtered users with their days
        users_with_filtered_days = await self.session.execute(subquery)
        users_with_filtered_days = users_with_filtered_days.scalars().all()

        # Filter users' days and leave only days where module_id is in module_ids
        for user in users_with_filtered_days:
            user.days = [day for day in user.days if day.module_id in module_ids]

        # Convert the filtered results to the desired format
        users_marks = self.__to_User_Marks(users_with_filtered_days)

        # Return the converted results
        return users_marks

    def __to_User_Marks(self, users_days: Iterable[UserDao]) -> List[UserMarks]:
        users_marks = []

        for user in users_days:

            user_marks = UserMarks(
                id=user.id,
                first_name=user.first_name,
                last_name=user.last_name,
                days=[]
            )
            users_marks.append(user_marks)
            for day in user.days:
                user_marks.days.append(self.__to_DayInfo(day))

        return users_marks


    def __to_DayInfo(self, day: DayDao):

        return DayInfo(
            id=day.id,
            presence=day.presence.type,
            type_of_mark=day.type_of_mark.type_of_mark,
            mark=day.mark,
            user_id=day.user_id,
            module_id=day.module_id,
            module_title=day.module.title,
            date=day.date
        )