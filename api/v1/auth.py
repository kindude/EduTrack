from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException
from starlette import status
from api.dependencies import get_auth_service
from schemas.token import Token, TokenRefreshNotFoundException
from schemas.user import UserAddRequest, UserExistsException, UserLogin, \
    WrongPasswordException, UserNotFoundException
from services.auth_service import AuthService


router = APIRouter()


@router.post("/register", status_code=status.HTTP_201_CREATED)
async def register_user(auth_service: Annotated[AuthService, Depends(get_auth_service)],
                        user_add: UserAddRequest):
    try:
        await auth_service.register_user(user_add=user_add)
        return status.HTTP_201_CREATED

    except UserExistsException as error:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT,
                            detail="User already exists" + str(error)) from error


@router.post("/login", status_code=status.HTTP_200_OK)
async def login_user(auth_service: Annotated[AuthService, Depends(get_auth_service)],
                     user_login: UserLogin) -> Token:
    try:
        return await auth_service.login(user_login)
    except WrongPasswordException as error:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail="Wrong password" + str(error)) from error
    except UserNotFoundException as error:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="User not found" + str(error)) from error


@router.post("/refresh", status_code=status.HTTP_200_OK)
async def refresh(request: Token, auth_service: Annotated[AuthService,
                                                Depends(get_auth_service)]) -> Token:
    try:
        return await auth_service.refresh(request)
    except TokenRefreshNotFoundException as error:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail="Token not found, log in again",
                            headers=auth_service.http_headers.WWW_AUTHENTICATE_BEARER) from error
