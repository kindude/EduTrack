"""
Модуль RefreshTokenRepository

Этот модуль содержит класс RefreshTokenRepository для работы с токенами обновления
    в хранилище кэша Redis.

Classes:
    - RefreshTokenRepository: Репозиторий для работы с токенами обновления
        в хранилище кэша Redis.

Attributes:
    - Redis: Класс Redis из модуля redis.
    - get_redis_session: Функция для получения сессии Redis из модуля repositories.db.
    - refresh_expiration: Переменная с настройкой времени истечения
            срока действия обновления токена.

Constants:
    - settings: Объект настроек JWT

Methods:
    - __init__: Инициализирует экземпляр репозитория.
    - save_item: Сохраняет элемент в хранилище кэша Redis с указанным ключом и значением.
    - get_item: Получает элемент из хранилища кэша Redis по указанному ключу.
"""

from typing import Union
from redis import Redis
from settings import JwtSettings

settings = JwtSettings()


class RefreshTokenRepository:
    """
    Репозиторий для работы с токенами обновления в хранилище кэша Redis.

    Args:
        session (Redis): Сессия Redis для выполнения операций с кэшем.
    """

    def __init__(self, session: Redis):
        """
        Инициализирует экземпляр репозитория.

        Args:
            session (Redis): Сессия базы данных.
        """

        self._redis = session

    async def save_item(self, key: str, value: str = "0") -> None:
        """
        Сохраняет элемент в хранилище кэша Redis с указанным ключом и значением.

        Args:
            key (str): Ключ, по которому элемент будет сохранен в кэше.
            value (str, optional): Значение элемента (по умолчанию - '0').

        Returns:
            None
        """

        await self._redis.set(key, value)
        await self._redis.expire(key, settings.refresh_expiration)

    async def get_item(self, key: str) -> Union[str, None]:
        """
        Получает элемент из хранилища кэша Redis по указанному ключу.

        Args:
            key (str): Ключ, по которому будет получен элемент из кэша.

        Returns:
            Union[str, None]: Значение элемента или None, если элемент не найден.
        """

        result = await self._redis.get(key)
        return result