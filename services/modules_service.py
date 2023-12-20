import uuid

from typing import Union

from sqlalchemy.exc import IntegrityError

from repositories.modules import ModulesRepository
from repositories.users import UsersRepository
from schemas.modules import ModuleInfo, ModuleExistsException, ModuleListResponse, Module, ModuleNotFoundException, \
    ModuleUpdateRequest


class ModulesService:
    """
    Сервис для работы с пользователями.
     Attributes:
        users_repo (UsersRepository): Репозиторий для пользователей.
    """

    def __init__(self, modules_repo: ModulesRepository):
        """
        Инициализация сервиса.

        Args:
             users_repo: Репозиторий для пользователей.
        """

        self.modules_repo = modules_repo

    async def get_modules(self) -> ModuleListResponse:
        modules = await self.modules_repo.get_all()
        return ModuleListResponse(
            modules=modules
        )

    async def get_module(self, module_alias: str) -> ModuleInfo:
        return await self.modules_repo.get_module_by_alias(module_alias=module_alias)

    async def add_module(self, add_module: ModuleInfo):
        try:

            module = Module(
                id=uuid.uuid4(),
                title=add_module.title,
                hours_taught=add_module.hours_taught,
                alias = add_module.alias
            )
            await self.modules_repo.add(add_module=module)
        except IntegrityError as exc:
            raise ModuleExistsException from exc

    async def update_module(self, module_id: uuid, update_module: ModuleUpdateRequest):
        module = await self.modules_repo.get_module_by_id(module_id=module_id)
        if not module:
            raise ModuleNotFoundException
        update_module = Module(
            id=module.id,
            alias=update_module.alias,
            title=update_module.title,
            hours_taught=update_module.hours_taught
        )
        await self.modules_repo.update_module(module_id=module_id, update_module=update_module)

    async def delete_module(self, module_name: str):
        await self.modules_repo.delete_module(module_name=module_name)
