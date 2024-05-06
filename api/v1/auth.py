"""
Модуль для обработки регистрации, аутентификации и обновления токенов пользователей.

Этот модуль предоставляет роутер FastAPI для выполнения операций,
    связанных с регистрацией пользователей, их аутентификацией и обновлением токенов.

"""

from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException, Response, Cookie
from starlette import status

from api.dependencies import get_auth_service
from schemas.access_token import AccessToken
from schemas.token import TokenRefreshNotFoundException, TokenExpiredException, TokenCorruptedException
from schemas.users.UserAuth0 import UserAuth0
from schemas.users.user import UserAddRequest, UserExistsException, UserLogin, WrongPasswordException, UserNotFoundException
from services.auth_service import AuthService

router = APIRouter()


@router.post("/register", status_code=status.HTTP_201_CREATED)
async def register_user(auth_service: Annotated[AuthService, Depends(get_auth_service)],
                        user_add: UserAddRequest) -> int:
    """
    Registers a new user.

        Args:
            auth_service (AuthService): Service to work with authorization.
            user_add (UserAddRequest): New user data.

        Returns:
            int: Status code HTTP 201 Created in case of successful registration.

        Raises:
            HTTPException: HTTP 409 Conflict, if a user exists.
    """

    try:
        await auth_service.register_user(user_add=user_add)
        return status.HTTP_201_CREATED

    except UserExistsException as error:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT,
                            detail="User already exists" + str(error)) from error


@router.post("/login", status_code=status.HTTP_200_OK)
async def login_user(auth_service: Annotated[AuthService, Depends(get_auth_service)],
                     user_login: UserLogin,
                     response: Response) -> AccessToken:
    """

    Аутентифицирует пользователя.

        Args:
            auth_service (AuthService): Сервис для работы с авторизациями.
            user_login (UserLogin): Данные для входа пользователя.
            response (Response): Объект ответа для установления cookies.

        Returns:
            TokensPair: Токен для аутентификации пользователя.

        Raises:
            HTTPException: HTTP 401 Unauthorized, если аутентификация не удалась.
            HTTPException: HTTP 404 Unauthorized, если пользователь не найден.

    """

    try:
        tokens_pair = await auth_service.login(user_login)
        response.set_cookie(key='refresh_token',
                            value=tokens_pair.refresh_token,
                            httponly=True)
        access_token = AccessToken(token=tokens_pair.access_token, type=tokens_pair.type)
        return access_token
    except WrongPasswordException as error:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail="Wrong password" + str(error)) from error
    except UserNotFoundException as error:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="User not found" + str(error)) from error


@router.post('/login-auth0', status_code=status.HTTP_200_OK)
async def login_with_auth0(auth_service: Annotated[AuthService, Depends(get_auth_service)], response:Response, user_login: UserAuth0) -> AccessToken:
    try:
        tokens_pair = await auth_service.login_with_auth0(user_login)
        response.set_cookie(key='refresh_token',
                            value=tokens_pair.refresh_token,
                            httponly=True)
        access_token = AccessToken(token=tokens_pair.access_token, type=tokens_pair.type)
        return access_token
    except:
        pass


@router.post("/logout", status_code=status.HTTP_200_OK)
async def logout_user(auth_service: Annotated[AuthService, Depends(get_auth_service)], response: Response,
                      refresh_token: Annotated[str | None, Cookie()] = None) -> Response:
    """
    Заканчивает сессию пользователя.

        :param auth_service: Сервис для работы с авторизациями.
        :param refresh_token: Токен обновления пользователя из куки.
        :return: Код статуса HTTP 200 OK при успешном выходе из сессии.
        :raise: HTTPException: HTTP 401 Unauthorized, если токен обновления не найден или его срок действия истёк.
    """

    try:
        response.delete_cookie('refresh_token')
        await auth_service.logout(refresh_token)
        response.status_code = 200
        return response
    except TokenRefreshNotFoundException as error:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail="Token not found, log in again",
                            headers=auth_service.http_headers.WWW_AUTHENTICATE_BEARER) from error
    except TokenExpiredException as error:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail="Token has expired, log in again",
                            headers=auth_service.http_headers.WWW_AUTHENTICATE_BEARER) from error


@router.post("/refresh", status_code=status.HTTP_200_OK)
async def refresh(auth_service: Annotated[AuthService, Depends(get_auth_service)],
                  response: Response,
                  refresh_token: Annotated[str | None, Cookie()] = None) -> AccessToken:
    """
    Обновляет токен пользователя для продления срока его действия.

        Args:
            refresh_token (str): Токен обновления пользователя из куки.
            auth_service (AuthService): Сервис для работы с авторизациями.
            response (Response): Объект ответа для установления cookies.

        Returns:
            TokensPair: Обновленный токен доступа.

        Raises:
            HTTPException: HTTP 401 Unauthorized, если токен обновления не найден или его срок действия истёк.
    """

    try:
        tokens_pair = await auth_service.refresh(refresh_token)
        response.set_cookie(key='refresh_token',
                            value=tokens_pair.refresh_token,
                            httponly=True)
        access_token = AccessToken(token=tokens_pair.access_token, type=tokens_pair.type)
        return access_token
    except TokenRefreshNotFoundException as error:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail="Token not found, log in again",
                            headers=auth_service.http_headers.WWW_AUTHENTICATE_BEARER) from error
    except TokenExpiredException as error:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail="Token has expired, log in again",
                            headers=auth_service.http_headers.WWW_AUTHENTICATE_BEARER) from error

    except TokenCorruptedException as error:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail="Token not found, log in again",
                            headers=auth_service.http_headers.WWW_AUTHENTICATE_BEARER) from error

