"""
Модель Token

Этот модуль содержит классы для моделирования токенов и исключений связанных с токенами.

Classes:
    - Token: Модель токена.
    - TokenException: Базовый класс исключения для токенов.
    - TokenUserNotFoundException: Исключение, возникающее при отсутствии пользователя,
            связанного с токеном.
    - TokenExpiredException: Исключение, возникающее при истечении срока действия токена.
    - TokenCorruptedException: Исключение, возникающее при повреждении токена.
    - TokenRefreshNotFoundException: Исключение, возникающее при отсутствии токена обновления.

Attributes:
    - BaseModel: Базовый класс модели Pydantic.
    - str: Строковой тип данных.

Fields:
    - access_token (str): Токен доступа.
    - refresh_token (str): Токен обновления.
    - type (str): Тип токена.

"""

from pydantic import BaseModel


class TokensPair(BaseModel):
    """
    Модель токена.

    Attributes:
        access_token (str): Значение токена доступа.
        refresh_token (str): Значение токена обновления.
        type (str): Тип токена.
    """

    access_token: str
    refresh_token: str
    type: str


class TokenException(Exception):
    """
    Базовый класс исключения для токенов.

    Этот класс является базовым для всех исключений, связанных с токенами.
    """


class TokenUserNotFoundException(TokenException):
    """
    Исключение, возникающее при отсутствии пользователя, связанного с токеном.

    Это исключение выбрасывается, когда токен не связан с пользователем.
    """


class TokenExpiredException(TokenException):
    """
    Исключение, возникающее при истечении срока действия токена.

    Это исключение выбрасывается, когда токен больше не действителен.
    """


class TokenCorruptedException(TokenException):
    """
    Исключение, возникающее при повреждении токена.

    Это исключение выбрасывается, когда токен поврежден или имеет неверный формат.
    """


class TokenRefreshNotFoundException(TokenException):
    """
    Исключение, возникающее при отсутствии токена обновления.

    Это исключение выбрасывается, когда токен обновления не найден.
    """
