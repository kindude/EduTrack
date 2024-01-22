"""
Модуль AuthService

Этот модуль содержит класс `AuthService`, предоставляющий методы для регистрации пользователей,
аутентификации и генерации токенов доступа.

Classes:
    - AuthService: Сервис для работы с авторизацией.

Attributes:
    - uuid: Класс UUID из модуля uuid.
    - IntegrityError: Исключение IntegrityError из модуля sqlalchemy.exc.
    - HttpHeaders: Класс HttpHeaders из модуля constants.http_headers.
    - PasswordHelper: Класс PasswordHelper из модуля helpers.password_helper.
    - RefreshTokenRepository: Класс RefreshTokenRepository из модуля repositories.refresh_token.
    - UsersRepository: Класс UsersRepository из модуля repositories.users.
    - TokensPair: Класс TokensPair из модуля schemas.token.
    - TokenRefreshNotFoundException: Исключение TokenRefreshNotFoundException
            из модуля schemas.token.
    - UserNotFoundException: Исключение UserNotFoundException из модуля schemas.users.
    - WrongPasswordException: Исключение WrongPasswordException из модуля schemas.users.
    - UserLogin: Класс UserLogin из модуля schemas.users.
    - UserExistsException: Исключение UserExistsException из модуля schemas.users.
    - User: Класс User из модуля schemas.users.
    - UserAddRequest: Класс UserAddRequest из модуля schemas.users.
    - JwtProcessorSingleton: Класс JwtProcessorSingleton из модуля services.token.
"""

import uuid

from sqlalchemy.exc import IntegrityError

from constants.http_headers import HttpHeaders
from helpers.password_helper import PasswordHelper
from models.user import Roles
from repositories.refresh_token import RefreshTokenRepository
from repositories.users import UsersRepository
from schemas.token import TokensPair, TokenCorruptedException
from schemas.users.user import UserAddRequest, User, UserExistsException, UserLogin, UserNotFoundException, \
    WrongPasswordException
from services.token import JwtProcessorSingleton


class AuthService:
    """
    Сервис для работы с авторизацией.
    """

    def __init__(self, users_repo: UsersRepository, refresh_token_repo: RefreshTokenRepository):
        """
        Конструктор AuthService

            :param users_repo: Репозиторий для работы с пользователями.
            :param refresh_token_repo: Репозиторий для работы с токенами
        """

        self.users_repo = users_repo
        self.password_helper = PasswordHelper()
        self.jwt_processor = JwtProcessorSingleton(session=self.users_repo.session)
        self.refresh_token_repo = refresh_token_repo
        self.http_headers = HttpHeaders()

    async def register_user(self, user_add: UserAddRequest) -> None:
        """
        Создание пользователя.

            :param user_add: Request на создание пользователя.
            :return: Ответ пользователя содержащий id добавленого пользователя.
            :raise: UserExistsException: Если пользователь уже существует.
        """

        try:
            user = User(
                id=uuid.uuid4(),
                first_name=user_add.first_name,
                last_name=user_add.last_name,
                address=user_add.address,
                city=user_add.city,
                phone_number=user_add.phone_number,
                email=user_add.email,
                password_hash=self.password_helper.hash_password(user_add.password),
                role=Roles.ADMIN
            )

            await self.users_repo.add(user=user)
        except IntegrityError as exc:
            raise UserExistsException from exc

    async def login(self, user_to_login: UserLogin) -> TokensPair:
        """
        Выполняет аутентификацию пользователя и генерирует токен доступа.

            :param user_to_login: Объект с данными для входа пользователя.
            :return: Объект, содержащий сгенерированный токен доступа.
            :raise:
                UserNotFoundException: Если пользователь с указанным адресом электронной почты не найден.
                WrongPasswordException: Если указанный пароль неверен.
        """

        user = await self.users_repo.get_by_email(email=user_to_login.email)
        if not user:
            raise UserNotFoundException
        if not self.password_helper.check_password(login_password=user_to_login.password,
                                                   password=user.password_hash):
            raise WrongPasswordException
        access_token, access_token_id = self.jwt_processor.access_jwt_processor.generate(
            user_id=user.id, role=user.role.value)
        refresh_token, refresh_token_id = self.jwt_processor.refresh_jwt_processor.generate(
            user_id=user.id, role=user.role.value)
        print(refresh_token)
        print(refresh_token_id)
        await self.refresh_token_repo.save_item(refresh_token_id)
        return TokensPair(access_token=access_token,
                          refresh_token=refresh_token,
                          type="bearer")

    async def logout(self, refresh_token: str) -> None:
        """
        Выполняет аутентификацию пользователя и генерирует токен доступа.

            :param refresh_token:
            :return: Токен обновления.
        """

        refresh_token_decode = self.jwt_processor.refresh_jwt_processor.decode(refresh_token)
        await self.refresh_token_repo.delete_item(refresh_token_decode.token_id)

    async def refresh(self, refresh_token: str) -> TokensPair:
        """
        Обновляет access-токен на основе refresh-токена.

            :param refresh_token: Токен аутентификации.
            :return: Обновленный access-токен.
            :raise:  TokenRefreshNotFoundException: Если refresh-токен не найден.
        """
        try:
            refresh_token_decode = self.jwt_processor.refresh_jwt_processor.decode(refresh_token)
            await self.refresh_token_repo.delete_item(refresh_token_decode.token_id)

            new_access_token, new_access_token_id = self.jwt_processor.access_jwt_processor.generate(
                user_id=refresh_token_decode.user_id,
                role=refresh_token_decode.role)
            new_refresh_token, new_refresh_token_id = self.jwt_processor.refresh_jwt_processor.generate(
                user_id=refresh_token_decode.user_id,
                role=refresh_token_decode.role)
            await self.refresh_token_repo.save_item(new_refresh_token_id)
        except AttributeError as error:
            raise TokenCorruptedException from error

        return TokensPair(
            access_token=new_access_token,
            refresh_token=new_refresh_token,
            type="bearer")
