"""
Модуль, содержащий функции и зависимости для обработки токенов и пользователей.

Этот модуль предоставляет функции для декодирования и обработки JWT-токенов,
получения информации о текущем пользователе, а также зависимости для работы с репозиториями
пользователей и обновлениями токенов.
"""

from fastapi import Depends, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from redis import Redis
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from constants.http_headers import HttpHeaders
from repositories.db import get_redis_session, get_async_session
from repositories.refresh_token import RefreshTokenRepository
from repositories.users import UsersRepository
from schemas.token import Token, TokenUserNotFoundException, TokenExpiredException, TokenCorruptedException
from schemas.user import UserRole, UserInfo
from services.token import JwtProcessorSingleton


# from repositories.db import get_async_session, get_redis_session
# from repositories.refresh_token import RefreshTokenRepository
# from repositories.users import UsersRepository
# from schemas.token import Token, TokenUserNotFoundException, TokenExpiredException, \
#     TokenCorruptedException
# from schemas.users import UserInfo, UserRole
# from services.token import JwtProcessorSingleton


def get_refresh_redis_repo(redis_session: Redis = Depends(get_redis_session)
                           ) -> RefreshTokenRepository:
    """
    Получает репозиторий для работы с обновлениями токенов Redis.

    Args:
        redis_session (Redis, optional): Сессия Redis. По умолчанию используется зависимость.

    Returns:
        RefreshTokenRepository: Репозиторий обновлений токенов Redis.
    """

    return RefreshTokenRepository(redis_session)


def get_users_repo(session: AsyncSession = Depends(get_async_session)) -> UsersRepository:
    """
    Получает репозиторий пользователей для работы с базой данных.

    Args:
        session (AsyncSession, optional): Сессия базы данных. По умолчанию используется зависимость.

    Returns:
        UsersRepository: Репозиторий пользователей.
    """

    return UsersRepository(session=session)


http_bearer = HTTPBearer()


def validate_token(access_token: HTTPAuthorizationCredentials = Depends(http_bearer), users_repo: UsersRepository = Depends(get_users_repo)
                   ) -> UserRole:
    """
    Декодирует и обрабатывает JWT-токен.

    Args:
        access_token: access_token в формате "Bearer...".
        users_repo (UsersRepository, optional): Репозиторий пользователей.
            По умолчанию используется зависимость.

    Returns:
        UserRole: Схема пользователя, содержащая роль.

    Raises:
        HTTPException: HTTP 401 Unauthorized, если пользователь не найден,
            токен истек, или токен поврежден.
    """

    try:
        if access_token is None:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                                detail="Authorization header is missing",
                                headers=HttpHeaders.WWW_AUTHENTICATE_BEARER)

        token = access_token.credentials
        jwt_processor = JwtProcessorSingleton(session=users_repo.session)
        user = jwt_processor.access_jwt_processor.decode(token=token)
        return user
    except TokenUserNotFoundException as error:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail="User not found",
                            headers=HttpHeaders.WWW_AUTHENTICATE_BEARER) from error
    except TokenExpiredException as error:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail="Token has expired",
                            headers=HttpHeaders.WWW_AUTHENTICATE_BEARER) from error
    except TokenCorruptedException as error:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail="Token is corrupted",
                            headers=HttpHeaders.WWW_AUTHENTICATE_BEARER) from error
    except AttributeError as error:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail="Token is corrupted",
                            headers=HttpHeaders.WWW_AUTHENTICATE_BEARER) from error


async def get_current_user(user: UserRole = Depends(validate_token),
                           users_repo: UsersRepository = Depends(get_users_repo)) -> UserInfo:
    """
    Получает информацию о текущем пользователе (авторизованном)
        на основе переданной схемы UserRole.

    Args:
        user (UserRole, optional): Идентификатор пользователя.
            По умолчанию используется зависимость
        users_repo (UsersRepository, optional): Репозиторий пользователей.
            По умолчанию используется зависимость.

    Returns:
        UserInfo: Информация о текущем пользователе.
    """

    return await users_repo.get_user(user_id=user.user_id)

