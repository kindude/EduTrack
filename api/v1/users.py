import uuid
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status

from api.dependencies import get_users_service
from api.dependencies_user import get_current_user, validate_token
from models.user import Roles

from schemas.users.user import UserListResponse, UserNotFoundException, \
    UsersNotFoundException, UserInfo, RoleNotFoundException, \
    UserRole, UserUpdateRequest, UserExistsException

from services.users_service import UsersService

router = APIRouter()


@router.get("/me", status_code=status.HTTP_200_OK)
async def get_me(current_user: UserInfo = Depends(get_current_user)) -> UserInfo:
    return current_user


@router.get("/", status_code=status.HTTP_200_OK)
async def get_all_users(user_service: Annotated[UsersService, Depends(get_users_service)],
                        current_user: UserRole = Depends(validate_token)) -> UserListResponse:
    try:
        if current_user.role != Roles.ADMIN.value:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                                detail="The list of users only allowed for admins")
        return await user_service.get_users()
    except UsersNotFoundException as error:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="Users not found" + str(error)) from error


@router.post("/all/teachers", status_code=status.HTTP_200_OK)
async def get_all_teachers(user_service: Annotated[UsersService, Depends(get_users_service)],
                            current_user: UserRole = Depends(validate_token)) -> UserListResponse:
    try:
        if current_user.role != Roles.ADMIN.value:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                                detail="The list of teachers only allowed for admins")
        return await user_service.get_users_by_role(role=Roles.TEACHER.value)
    except UsersNotFoundException as error:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="Suppliers not found" + str(error)) from error
    except RoleNotFoundException as error:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="Role not found" + str(error)) from error


@router.post("/all/students", status_code=status.HTTP_200_OK)
async def get_all_students(user_service: Annotated[UsersService, Depends(get_users_service)],
                          current_user: UserRole = Depends(validate_token)) -> UserListResponse:
    try:
        if current_user.role != Roles.ADMIN.value:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                                detail="The list of students only allowed for admins")
        return await user_service.get_users_by_role(role=Roles.STUDENT.value)
    except UsersNotFoundException as error:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="Clients not found" + str(error)) from error
    except RoleNotFoundException as error:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="Role not found" + str(error)) from error


@router.post("/all/admins", status_code=status.HTTP_200_OK)
async def get_all_admins(user_service: Annotated[UsersService, Depends(get_users_service)],
                         current_user: UserRole = Depends(validate_token)) -> UserListResponse:
    try:
        if current_user.role != Roles.ADMIN.value:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                                detail="The list of admins only allowed for admins")
        return await user_service.get_users_by_role(role=Roles.ADMIN.value)
    except UsersNotFoundException as error:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="Admins not found" + str(error)) from error
    except RoleNotFoundException as error:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="Role not found" + str(error)) from error


@router.get("/{user_id}", status_code=status.HTTP_200_OK)
async def get_user(user_id: uuid.UUID, user_service: Annotated[UsersService, Depends(get_users_service)]
                   ) -> UserInfo:
    try:
        return await user_service.get_user(user_id=user_id)
    except UserNotFoundException as error:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="User not found" + str(error)) from error


@router.put("/", status_code=status.HTTP_200_OK)
async def update_user(update_user_: UserUpdateRequest,
                      user_service: Annotated[UsersService, Depends(get_users_service)], current_user: UserInfo = Depends(get_current_user)):
    try:

        await user_service.update_user(update_user=update_user_)
        return status.HTTP_200_OK
    except UserExistsException as exc:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT,
                            detail="User exists" + str(exc)) from exc


@router.delete('/{user_id}', status_code=status.HTTP_200_OK)
async def delete_user(user_id: uuid.UUID, user_service: Annotated[UsersService, Depends(get_users_service)],
                      current_user: UserInfo = Depends(get_current_user)):

    try:
        if (current_user.id != user_id) or (current_user.role != Roles.ADMIN):
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                                detail="You are not allowed to delete this profile")
        await user_service.delete_user(user_id)
        return status.HTTP_200_OK
    except:
        pass

