"""
Модуль database

Этот модуль содержит функции и настройки для работы с базой данных.

Attributes:
    - AsyncSession: Класс AsyncSession из модуля sqlalchemy.ext.asyncio.
    - async_sessionmaker: Функция async_sessionmaker из модуля sqlalchemy.ext.asyncio.
    - create_async_engine: Функция create_async_engine из модуля sqlalchemy.ext.asyncio.

Constants:
    - settings: Объект настроек подключения к БД
    - engine: Объект SQLAlchemy для работы с базой данных.
    - async_session_maker: Функция для создания асинхронных сессий SQLAlchemy.

Functions:
    - get_async_session: Получает асинхронную сессию для взаимодействия с базой данных.
    - get_redis_session: Получает сессию Redis для выполнения операций с кэшем.
"""

from sqlalchemy.ext.asyncio import (AsyncSession, async_sessionmaker,
                                    create_async_engine)
from redis.asyncio import Redis
from settings import DatabaseSettings

settings = DatabaseSettings()
engine = create_async_engine(settings.postgres_url.unicode_string(), echo=True)
async_session_maker = async_sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)


async def get_async_session() -> AsyncSession:
    """
       Получает асинхронную сессию для взаимодействия с базой данных.

       Returns:
           AsyncSession: Асинхронная сессия SQLAlchemy.
       """

    async with async_session_maker() as session:
        try:
            yield session
        finally:
            await session.close()


async def get_redis_session() -> Redis:
    """
    Получает сессию Redis для выполнения операций с кэшем.

    Returns:
        redis.Redis: Сессия Redis.
    """

    return Redis.from_url(settings.redis_url.unicode_string())
