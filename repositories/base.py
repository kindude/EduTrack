"""
Модуль BaseRepository

Этот модуль содержит абстрактный базовый класс `BaseRepository` для репозиториев.

Classes:
    BaseRepository: Абстрактный базовый класс для репозиториев.

Attributes:
    - ABC: Класс ABC из модуля abc.
    - Any: Тип Any из модуля typing.
    - Dict: Тип Dict из модуля typing.
    - Type: Тип Type из модуля typing.
    - List: Тип List из модуля typing.
    - Union: Тип Union из модуля typing.
    - insert: Функция insert из модуля sqlalchemy.
    - select: Функция select из модуля sqlalchemy.
    - AsyncSession: Класс AsyncSession из модуля sqlalchemy.ext.asyncio.
    - Base: Класс Base из модуля models.base.
    - uuid: Модуль uuid.
"""

import uuid

from abc import ABC, abstractmethod
from typing import Any, Dict, Type, List, Union, Iterable
from sqlalchemy import insert, select, update, delete
from sqlalchemy.ext.asyncio import AsyncSession
from models.base import Base


class BaseRepository(ABC):
    """
    Абстрактный базовый класс для репозиториев.

    Attributes:
        session (AsyncSession): Сессия базы данных для взаимодействия с данными.
    """

    def __init__(self, session: AsyncSession):
        """
        Инициализирует экземпляр репозитория.

        Args:
            session (AsyncSession): Сессия базы данных.
        """

        self.session = session

    @property
    @abstractmethod
    def model(self) -> Type[Base]:
        """
        Абстрактное свойство, представляющее модель данных репозитория.

        Returns:
            Type[Base]: Класс модели данных.
        """

    async def _add(self, model: Dict[str, Any]) -> Base:
        """
        Adds a new record in the database.

        Args:
            model (Dict[str, Any]): Data to add.

        Returns:
            Base: Added record.
        """

        stmt_to_insert = insert(self.model).values(model).returning(self.model)
        result = await self.session.execute(stmt_to_insert)
        await self.session.commit()
        return result

    async def _update(self, _id: Union[uuid, int], model: Dict[str, Any]) -> Base:
        stmt_to_update = update(self.model).values(model).filter(self.model.id == _id).returning(self.model)
        result = await self.session.execute(stmt_to_update)
        await self.session.commit()
        return result

    async def _get(self, _id: Union[uuid, int]) -> Base:
        """
        Получает запись по идентификатору.

        Args:
            _id (Union[uuid.UUID, int]): Идентификатор записи.

        Returns:
            Base: Запись с указанным идентификатором.
        """

        stmt_to_select_one = select(self.model).filter(self.model.id == _id)
        item = await self.session.execute(stmt_to_select_one)
        return item.scalar_one_or_none()

    async def _get_all(self) -> Iterable[Base]:
        """
        Получает список всех записей.

        Returns:
            List[Base]: Список всех записей.
        """

        stmt_to_select_all = select(self.model)
        items = await self.session.execute(stmt_to_select_all)
        return items.scalars().all()

    async def _delete(self, id: uuid.UUID) -> None:
        try:
            stmt_to_delete = delete(self.model).filter(self.model.id == id)
            await self.session.execute(stmt_to_delete)
            await self.session.commit()
        except Exception as exc:
            print(exc)

