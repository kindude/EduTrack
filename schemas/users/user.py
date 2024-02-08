"""
Модуль, содержащий определения Pydantic-моделей и исключений для представления
    данных о пользователях.

Classes:
    UserInfo: Модель данных о пользователе.
    User: Модель данных пользователя с расширенными полями.
    UserAddRequest: Модель запроса на добавление пользователя.
    UserListResponse: Модель списка пользователей в ответе.
    UserLogin: Модель для входа пользователя в систему.
    UserException: Базовый класс исключений, связанных с пользователями.
    UserNotFoundException: Исключение, возникающее, когда пользователь
        не найден в базе данных.
    UsersNotFoundException: Исключение, возникающее, когда не найдено
        ни одного пользователя в базе данных.
    WrongPasswordException: Исключение, возникающее, когда пароль неверный.
    UserExistsException: Исключение, возникающее, когда попытка добавления
        существующего пользователя.
"""

import uuid

from typing import List
from pydantic import BaseModel, constr, EmailStr
from pydantic_extra_types.phone_numbers import PhoneNumber

from models.user import Roles
from schemas.base import BaseSchema


class UserInfo(BaseSchema):
    """
    Представляет данные о пользователе.

    Attributes:
        first_name (str): Имя пользователя.
        last_name (str): Фамилия пользователя.
        phone_number (PhoneNumber): Номер телефона пользователя.
        city (str): Город пользователя.
        address (str): Адрес пользователя.
        email (EmailStr): Адрес электронной почты пользователя.
        role (str): Роль пользователя в системе.
    """

    id: uuid.UUID
    first_name: constr(max_length=50, min_length=1)
    last_name: constr(max_length=50, min_length=1)
    phone_number: PhoneNumber
    city: constr(max_length=50, min_length=1)
    address: constr(max_length=50, min_length=5)
    email: EmailStr
    role: Roles

    class Config:
        """
        Класс конфигурации для модели UserInfo.

        Attributes:
            arbitrary_types_allowed (bool): Разрешает использование произвольных типов.
            from_attributes (bool): Позволяет инициализировать объект модели из атрибутов.
        """

        arbitrary_types_allowed = True
        from_attributes = True


class User(UserInfo):
    """
    Представляет пользователя с расширенными полями.

    Attributes:
        id (uuid.UUID): Уникальный идентификатор пользователя.
        password_hash (str): Хэш пароля пользователя.
    """

    id: uuid
    password_hash: constr(max_length=300, min_length=8)

    class Config:
        """
        Класс конфигурации для модели User.

        Attributes:
            arbitrary_types_allowed (bool): Разрешает использование произвольных типов.
            from_attributes (bool): Позволяет инициализировать объект модели из атрибутов.
        """

        arbitrary_types_allowed = True
        from_attributes = True


class UserAddRequest(BaseSchema):
    """
    Модель запроса на добавление пользователя.

    Attributes:
        password (str): Пароль пользователя.
    """

    first_name: constr(max_length=50, min_length=1)
    last_name: constr(max_length=50, min_length=1)
    phone_number: PhoneNumber
    city: constr(max_length=50, min_length=1)
    address: constr(max_length=50, min_length=5)
    email: EmailStr
    password: constr(max_length=300, min_length=8)

    class Config:
        """
        Класс конфигурации для модели UserAddRequest.

        Attributes:
            arbitrary_types_allowed (bool): Разрешает использование произвольных типов.
            from_attributes (bool): Позволяет инициализировать объект модели из атрибутов.
        """

        arbitrary_types_allowed = True
        from_attributes = True


class UserUpdateRequest(BaseModel):
    """
    Данные для обновления пользователя.

    Attributes:
        id (uuid.UUID): Уникальный идентификатор пользователя.
        first_name (str): Имя пользователя.
        last_name (str): Фамилия пользователя.
        phone_number (PhoneNumber): Номер телефона пользователя.
        password (str): Пароль пользователя.
        city (str): Город пользователя.
        address (str): Адрес пользователя.
        email (EmailStr): Адрес электронной почты пользователя.
        role (str): Роль пользователя в системе.
    """

    id: uuid
    first_name: constr(max_length=50, min_length=1)
    last_name: constr(max_length=50, min_length=1)
    phone_number: PhoneNumber
    password: constr(max_length=300, min_length=8)
    city: constr(max_length=50, min_length=1)
    address: constr(max_length=50, min_length=5)
    email: EmailStr
    role: Roles

    class Config:
        """
        Класс конфигурации для модели UserUpdateRequest.

        Attributes:
            arbitrary_types_allowed (bool): Разрешает использование произвольных типов.
            from_attributes (bool): Позволяет инициализировать объект модели из атрибутов.
        """

        arbitrary_types_allowed = True
        from_attributes = True


class UserListResponse(BaseModel):
    """
    Модель списка пользователей в ответе.

    Attributes:
        users (List[User]): Список пользователей.
    """

    users: List[UserInfo]

    class Config:
        """
        Класс конфигурации для модели UserListResponse.

        Attributes:
            arbitrary_types_allowed (bool): Разрешает использование произвольных типов.
            from_attributes (bool): Позволяет инициализировать объект модели из атрибутов.
        """

        arbitrary_types_allowed = True
        from_attributes = True


class UserLogin(BaseModel):
    """
    Модель для входа пользователя в систему.

    Attributes:
        email (str): Адрес электронной почты пользователя.
        password (str): Пароль пользователя.
    """

    email: constr(max_length=50, min_length=1)
    password: constr(max_length=300, min_length=8)

    class Config:
        """
        Класс конфигурации для модели UserLogin.

        Attributes:
            arbitrary_types_allowed (bool): Разрешает использование произвольных типов.
            from_attributes (bool): Позволяет инициализировать объект модели из атрибутов.
        """

        arbitrary_types_allowed = True
        from_attributes = True


class UserRole(BaseModel):
    """
    Модель данных для роли пользователя.

    Attributes:
        token_id (str): Уникальный идентификатор токена.
        user_id (str): Идентификатор пользователя.
        role (str): Роль пользователя.
    """

    token_id: str
    user_id: uuid
    role: str

    class Config:
        """
        Класс конфигурации для модели UserRole.

        Attributes:
            arbitrary_types_allowed (bool): Разрешает использование произвольных типов.
            from_attributes (bool): Позволяет инициализировать объект модели из атрибутов.
        """

        arbitrary_types_allowed = True
        from_attributes = True


class UserException(Exception):
    """
    Обработка ошибок, связанных с пользователями.
    """


class UserNotFoundException(UserException):
    """
    Обработка ошибок, связанных с тем, что не найдено ни одного пользователя в базе данных.
    """


class UsersNotFoundException(UserException):
    """
    Обработка ошибок, связанных с тем, что не найдено ни одного пользователя в базе данных.
    """


class WrongPasswordException(UserException):
    """
    Обработка ошибок с неправильным паролем
    """


class UserExistsException(UserException):
    """
    Обработка ошибки при попытке добавить существующего пользователя
    """


class RoleNotFoundException(UserException):
    """
    Обработка ошибки при попытке получить пользователей с несуществующей ролью
    """
