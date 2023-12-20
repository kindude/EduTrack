import uuid

from sqlalchemy import select
from sqlalchemy.orm import selectinload

from models.action import ActionDao
from models.user import UserDao
from repositories.base import BaseRepository
from schemas.actions.action import Action


class ActionsRepository(BaseRepository):


    model = ActionDao

    async def add_action(self, action: Action) -> None:
        await self._add(action.model_dump())

    async def get_users_by_module_id(self, module_id: uuid.UUID):
        stmt_to_select_users = select(ActionDao).filter(ActionDao.module_id == module_id).options(
            selectinload(ActionDao.user))
        actions = await self.session.execute(stmt_to_select_users)
        actions = actions.scalars().all()
        print(actions[0].user.email)


    async def get_modules_by_user_id(self, user_id: uuid.UUID):
        stmt_to_select_modules = select(ActionDao).filter(ActionDao.user_id == user_id).options(
            selectinload(ActionDao.module))
        actions = await self.session.execute(stmt_to_select_modules)
        actions = actions.scalars().all()
        print(actions[0].module.title)
