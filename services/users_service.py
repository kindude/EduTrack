"""
Модуль `users_service.py` предоставляет сервис для работы с пользователями в базе данных.

Содержит класс `UsersService`, который предоставляет методы для регистрации,
    аутентификации пользователей, а также получения информации о пользователях.

Attributes:
    users_repo (UsersRepository): Репозиторий для пользователей.
"""


import uuid

from typing import Union

from sqlalchemy.exc import IntegrityError

from helpers.password_helper import PasswordHelper
from repositories.images_repo import ImagesRepository
from repositories.users import UsersRepository
from schemas.images.image_add_request import ImageAddRequest
from schemas.users.user import UserListResponse, UserNotFoundException, \
    UsersNotFoundException, UserInfo, UserUpdateRequest, UserExistsException, User


class UsersService:
    """
    Сервис для работы с пользователями.
     Attributes:
        users_repo (UsersRepository): Репозиторий для пользователей.
    """

    def __init__(self, users_repo: UsersRepository, images_repo: ImagesRepository):
        """
        Инициализация сервиса.

        Args:
             users_repo: Репозиторий для пользователей.
        """

        self.users_repo = users_repo
        self.images_repo = images_repo
        self.password_helper = PasswordHelper()

    async def get_users(self) -> UserListResponse:
        """
        Получение списка пользователей.

        Returns:
            UserListResponse: Список пользователей.

        Raises:
            UsersNotFoundException: Если не удалось получить список пользователей.
        """

        users = await self.users_repo.get_all()
        if not users:
            raise UsersNotFoundException
        return users

    async def get_users_by_role(self, role: str) -> UserListResponse:
        """
        Получает список пользователей по указанной роли.

        Args:
            role (str): Роль пользователей для фильтрации.

        Returns:
            UserListResponse: Список пользователей с указанной ролью.

        Raises:
            UsersNotFoundException: Если не найдено пользователей с указанной ролью.
        """

        users = await self.users_repo.get_users_by_role(role=role)
        if users:
            return users
        raise UsersNotFoundException

    async def get_user(self,  user_id: Union[uuid, int]) -> UserInfo:
        """
        Получает данные о пользователе по его идентификатору.

        Args:
            user_id (Union[uuid.UUID, int]): Идентификатор пользователя.

        Returns:
            User: Объект пользовательских данных.

        Raises:
            UserNotFoundException: Если не удалось получить пользователя.
        """

        try:
            user = await self.users_repo.get_user(user_id=user_id)
            if not user:
                raise UserNotFoundException
            return user
        except TypeError as error:
            raise UserNotFoundException from error

    async def update_user(self, update_user: UserUpdateRequest) -> None:
        """
        Обновляет информацию о пользователе.

        Args:
            update_user (UserUpdateRequest): Объект запроса на обновление информации о пользователе.

        Raises:
            UserExistsException: Если пользователь с такими данными уже существует.
        """

        user = User(
            id=update_user.id,
            first_name=update_user.first_name,
            last_name=update_user.last_name,
            phone_number=update_user.phone_number,
            city=update_user.city,
            address=update_user.address,
            email=update_user.email,
            password_hash=self.password_helper.hash_password(update_user.password),
            role=update_user.role
        )
        try:
            await self.users_repo.update_user(user=user)
        except IntegrityError as error:
            raise UserExistsException from error

    async def add_image(self, image_add_request: ImageAddRequest):
        await self.images_repo.add_image(image_add=image_add_request)

    async def delete_user(self, user_id: uuid.UUID) -> None:
        try:
            await self.users_repo.delete_user(user_id)
        except Exception as exc:
            print(exc)


