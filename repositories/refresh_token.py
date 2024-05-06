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

from schemas.token import TokenRefreshNotFoundException
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

        await self._redis.set(key, value)
        await self._redis.expire(key, settings.refresh_expiration)

    async def get_item(self, key: str) -> Union[str, None]:

        result = await self._redis.get(key)
        return result

    async def get_items(self):
        keys = [key.decode() for key in await self._redis.keys("*")]
        results = {key: await self._redis.get(key) for key in keys}
        return results

    async def delete_item(self, key: str) -> None:
        """
        Удаляет элемент из хранилища кэша Redis по указанному ключу.

        Args:
            key (str): Ключ, по которому будет удалён элемент из кэша.
        """

        result = await self._redis.get(key)
        if not result:
            raise TokenRefreshNotFoundException
        await self._redis.delete(key)
