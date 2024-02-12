"""
Модуль users_repository

Этот модуль содержит репозиторий для работы с данными пользователей в базе данных.

Attributes:
    - uuid: Модуль uuid для работы с UUID.
    - Union: Тип Union из модуля typing.
    - select: Функция select из модуля sqlalchemy для создания SQL-запросов SELECT.
    - UserDao: Класс модели данных пользователей (UserDao).
    - BaseRepository: Класс базового репозитория для работы с данными.

Classes:
    - UsersRepository: Класс репозитория для взаимодействия с данными пользователей в базе данных.

Constants:
    - model: Класс модели данных пользователей (UserDao).
"""

import uuid

from typing import Union
from sqlalchemy import select, update

from models.user import UserDao, Roles
from repositories.base import BaseRepository
from schemas.users.user import User, UserListResponse, UserInfo, RoleNotFoundException


class UsersRepository(BaseRepository):
    """
    Репозиторий для взаимодействия с данными пользователей в базе данных.

    Attributes:
        model (Base): Модель базы данных, представляющая пользовательские данные.
    """

    model = UserDao

    async def add(self, user: User) -> User:
        """
        Добавляет нового пользователя в базу данных.

        Args:
           user (User): Данные пользователя.

        """

        await self._add(user.model_dump())
        return user

    async def get_all(self) -> UserListResponse:

        """
        Получает список всех пользователей из базы данных.

        Returns:
        List[UserDao]: Список пользователей.
        """

        users = await self._get_all()
        users = [UserInfo.model_validate(user) for user in users]
        return UserListResponse(users=users)

    async def get_users_by_role(self, role: str) -> Union[UserListResponse, None]:
        """
        Получает список пользователей по указанной роли.

        Args:
            role (str): Роль пользователей.

        Returns:
            Union[UserListResponse, None]: Список пользователей с указанной ролью или None,
                если пользователей нет.

        Raises:
            RoleNotFoundException: Если указанная роль недействительна.
        """

        if role not in Roles.__members__:
            raise RoleNotFoundException(f"Invalid role: {role}")
        role_enum_member = Roles.__members__.get(role)
        stmt_to_select_users_by_role = select(self.model).filter(
            self.model.role == role_enum_member)
        users = (await self.session.execute(stmt_to_select_users_by_role)).scalars().all()
        if not users:
            return None
        users = [UserInfo.from_orm(user) for user in users]
        return UserListResponse(users=users)

    async def get_user(self, user_id: uuid) -> UserInfo:
        """
        Получает данные о пользователе по его идентификатору.

        Args:
            user_id (Union[uuid.UUID, int]): Идентификатор пользователя.

        Returns:
            UserDao: Данные о пользователе.
        """

        user = await self._get(_id=user_id)
        user.role = user.role.value
        return UserInfo.model_validate(user)

    async def get_by_email(self, email: str) -> Union[User, None]:
        """
        Получает данные о пользователе по его адресу электронной почты.

        Args:
            email (str): Адрес электронной почты пользователя.

        Returns:
            UserDao | None: Данные о пользователе, если пользователь найден, иначе None.
        """

        stmt_to_select_one = select(self.model).filter(self.model.email == email)
        item = await self.session.execute(stmt_to_select_one)
        item = item.scalar_one_or_none()
        if item:
            return User.model_validate(item)


    async def update_user(self, user: User) -> None:
        """
        Обновляет данные пользователя

        Args:
            user (User): Новые данные пользователя.
        """

        stmt_to_update_user = update(self.model).values(user.model_dump()).filter(UserDao.email == user.email)
        await self.session.execute(stmt_to_update_user)
        await self.session.commit()

    async def delete_user(self, user_id: uuid.UUID) -> None:
        try:
            await self._delete(user_id)
        except Exception as exc:
            print(exc)
