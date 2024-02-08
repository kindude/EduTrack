import uuid
from typing import List
from sqlalchemy import select, delete, func

from models.module import ModuleDao
from repositories.base import BaseRepository
from schemas.modules.module import Module
from schemas.modules.module_info import ModuleInfo


class ModulesRepository(BaseRepository):

    model = ModuleDao

    async def add(self, add_module: Module) -> None:
        await self._add(add_module.model_dump())

    async def get_all(self) -> List[ModuleInfo]:
        modules = await self._get_all()
        if not modules:
            return []
        modules = [ModuleInfo.model_validate(module) for module in modules]
        return modules

    #
    # async def get_module_by_id(self, module_id: uuid) -> Module:
    #     module = await self._get(_id=module_id)
    #     if not module:
    #         raise ModuleNotFoundException
    #     return Module.model_validate(module)
    #
    # async def get_module_by_name(self, module_name: str) -> ModuleInfo:
    #     stmt_to_select_one = select(ModuleDao).filter(ModuleDao.title == module_name)
    #     module = await self.session.execute(stmt_to_select_one)
    #     module = module.scalar_one_or_none()
    #     return ModuleInfo.model_validate(module)
    #
    # async def get_module_by_alias(self, module_alias: str) -> ModuleInfo:
    #     stmt_to_select_one = select(ModuleDao).filter(func.lower(ModuleDao.alias) == module_alias.lower())
    #     module = await self.session.execute(stmt_to_select_one)
    #     module = module.scalar_one_or_none()
    #     if not module:
    #         raise ModuleNotFoundException
    #     return ModuleInfo.model_validate(module)
    #
    # async def delete_module(self, module_name: str) -> None:
    #     stmt_to_delete_module = delete(ModuleDao).filter(ModuleDao.title == module_name)
    #     await self.session.execute(stmt_to_delete_module)
    #     await self.session.commit()
    #
    # async def update_module(self, module_id: uuid, update_module: Module):
    #     try:
    #         await self._update(_id=module_id, model=update_module.model_dump())
    #     except TypeError as error:
    #         raise ModuleNotFoundException from error
