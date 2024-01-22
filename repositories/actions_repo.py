import uuid
from typing import List, Union

from sqlalchemy import select
from sqlalchemy.orm import selectinload

from models.action import ActionDao
from repositories.base import BaseRepository
from schemas.actions.action import Action
from schemas.modules.module_info import ModuleInfo
from schemas.modules.module_users import ModuleUsers
from schemas.users.user import UserInfo


class ActionsRepository(BaseRepository):


    model = ActionDao

    async def add_action(self, action: Action) -> None:
        await self._add(action.model_dump())

    async def get_users_by_module_id(self, module_id: uuid.UUID) -> ModuleUsers:
        stmt_to_select_users = select(ActionDao).filter(ActionDao.module_id == module_id).options(
            selectinload(ActionDao.user),
            selectinload(ActionDao.module))
        actions = await self.session.execute(stmt_to_select_users)
        actions = actions.scalars().all()
        users = [UserInfo.model_validate(action.user) for action in actions]
        module = ModuleInfo.model_validate(actions[0].module)
        return ModuleUsers(
            module=module,
            users=users
        )

    async def get_modules_by_user_id(self, user_id: uuid.UUID) -> List[ModuleInfo]:
        stmt_to_select_modules = select(ActionDao).filter(ActionDao.user_id == user_id).options(
            selectinload(ActionDao.module))
        actions = await self.session.execute(stmt_to_select_modules)
        actions = actions.scalars().all()
        return [ModuleInfo.model_validate(action.module) for action in actions]

    async def get_action_by_module_id(self, module_id: uuid.UUID) -> Union[UserInfo, str]:
        stmt_to_select_action = select(ActionDao).options(selectinload(ActionDao.user)).filter(ActionDao.module_id == module_id and ActionDao.role == 'TEACHER').limit(1)
        action = await self.session.execute(stmt_to_select_action)
        action = action.scalar_one_or_none()
        if not action:
            return 'N/A'
        user = UserInfo.model_validate(action.user)
        return user
