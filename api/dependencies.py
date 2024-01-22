"""
Модуль dependencies.py содержит определение зависимостей для приложения.

Этот модуль включает в себя функции для создания экземпляров сервисов, используемых в приложении.
"""

from redis import Redis
from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from repositories.actions_repo import ActionsRepository
from repositories.days_repository import DaysRepository
from repositories.modules import ModulesRepository
from repositories.db import get_async_session, get_redis_session
from repositories.posts_repository import PostsRepository
from repositories.refresh_token import RefreshTokenRepository
from repositories.users import UsersRepository
from services.actions_service import ActionsService
from services.auth_service import AuthService
from services.days_service import DaysService
from services.modules_service import ModulesService
from services.posts_service import PostsService
from services.statistics_service import StatisticsService
from services.users_service import UsersService


def get_users_service(session: AsyncSession = Depends(get_async_session)) -> UsersService:
    """
    Получает сервис для работы с пользователями.

    Args:
        session (AsyncSession): Асинхронная сессия базы данных.

    Returns:
        UsersService: Сервис для работы с пользователями.
    """

    users_repo = UsersRepository(session=session)
    return UsersService(users_repo=users_repo)


def get_auth_service(session: AsyncSession = Depends(get_async_session),
                     redis_session: Redis = Depends(get_redis_session)) -> AuthService:
    """
    Получает сервис для работы с пользователями.

    Args:
        session (AsyncSession): Асинхронная сессия базы данных
        redis_session (Redis): Сессия для работы с Redis

    Returns:
        AuthService: Сервис для работы с функциями авторизации.
    """

    users_repo = UsersRepository(session=session)
    refresh_token_repo = RefreshTokenRepository(session=redis_session)
    return AuthService(users_repo=users_repo, refresh_token_repo=refresh_token_repo)


def get_modules_service(session: AsyncSession = Depends(get_async_session)) -> ModulesService:
    """
    Получает сервис для работы с пользователями.

    Args:
        session (AsyncSession): Асинхронная сессия базы данных.

    Returns:
        UsersService: Сервис для работы с пользователями.
    """

    modules_repo = ModulesRepository(session=session)
    actions_repo = ActionsRepository(session=session)

    return ModulesService(modules_repo=modules_repo, actions_repo=actions_repo)


def get_actions_service(session: AsyncSession = Depends(get_async_session)) -> ActionsService:

    actions_repo = ActionsRepository(session=session)
    return ActionsService(actions_repo=actions_repo)


def get_days_service(session: AsyncSession = Depends(get_async_session)) -> DaysService:
    days_repo = DaysRepository(session=session)
    return DaysService(days_repo=days_repo)


def get_statistics_service(session: AsyncSession = Depends(get_async_session)) -> StatisticsService:
    days_repo = DaysRepository(session=session)
    return StatisticsService(days_repo=days_repo)


def get_posts_service(session: AsyncSession = Depends(get_async_session)) -> PostsService:
    posts_repo = PostsRepository(session=session)
    return PostsService(posts_repo=posts_repo)


