import uuid
from typing import List

from sqlalchemy.exc import IntegrityError

from repositories.actions_repo import ActionsRepository
from repositories.modules import ModulesRepository
from repositories.users import UsersRepository
from schemas.modules.module import Module
from schemas.modules.module_add_request import ModuleAddRequest
from schemas.modules.module_exceptions import ModuleExistsException
from schemas.modules.module_info import ModuleInfo
from schemas.modules.module_users import ModuleUsers


class ModulesService:
    """
    Сервис для работы с пользователями.
     Attributes:
        users_repo (UsersRepository): Репозиторий для пользователей.
    """

    def __init__(self, modules_repo: ModulesRepository, actions_repo: ActionsRepository):
        """
        Инициализация сервиса.

        Args:
             users_repo: Репозиторий для пользователей.
        """

        self.modules_repo = modules_repo
        self.actions_repo = actions_repo

    async def get_modules(self) -> List[ModuleUsers]:

        modules = await self.modules_repo.get_all()
        modules_with_lecturer = []

        for module in modules:
            user = await self.actions_repo.get_action_by_module_id(module_id=module.id)
            if user != 'N/A':
                modules_with_lecturer.append(ModuleUsers(
                    module=module,
                    users=[user]
                ))
            else:
                modules_with_lecturer.append(ModuleUsers(
                    module=module,
                    users=[]
                ))
        return modules_with_lecturer


    # async def get_module(self, module_alias: str) -> ModuleInfo:
    #     return await self.modules_repo.get_module_by_alias(module_alias=module_alias)

    async def add_module(self, add_module: ModuleAddRequest):
        try:

            module = Module(
                id=uuid.uuid4(),
                title=add_module.title,
                hours_taught=add_module.hours_taught,
                alias=add_module.alias
            )
            await self.modules_repo.add(add_module=module)
        except IntegrityError as exc:
            raise ModuleExistsException from exc

    # async def update_module(self, module_id: uuid, update_module: ModuleUpdateRequest):
    #     module = await self.modules_repo.get_module_by_id(module_id=module_id)
    #     if not module:
    #         raise ModuleNotFoundException
    #     update_module = Module(
    #         id=module.id,
    #         alias=update_module.alias,
    #         title=update_module.title,
    #         hours_taught=update_module.hours_taught
    #     )
    #     await self.modules_repo.update_module(module_id=module_id, update_module=update_module)
    #
    # async def delete_module(self, module_name: str):
    #     await self.modules_repo.delete_module(module_name=module_name)
