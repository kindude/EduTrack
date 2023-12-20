import uuid
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from starlette import status

from api.dependencies import get_modules_service
from api.dependencies_user import validate_token
from models.user import Roles
from schemas.modules import ModuleInfo, ModuleListResponse, ModuleExistsException, ModuleNotFoundException, \
    ModulesNotFoundException, ModuleUpdateRequest
from schemas.user import UserRole
from services.modules_service import ModulesService

router = APIRouter()


@router.get("/all", status_code=status.HTTP_200_OK)
async def get_modules(module_service: Annotated[ModulesService, Depends(get_modules_service)]) -> ModuleListResponse:
    try:
        return await module_service.get_modules()
    except ModulesNotFoundException:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="modules not found")


@router.get("/{module_alias}", status_code=status.HTTP_200_OK)
async def get_module(module_alias: str, module_service: Annotated[ModulesService, Depends(get_modules_service)]
                     ) -> ModuleInfo:
    try:
        return await module_service.get_module(module_alias=module_alias)
    except ModuleNotFoundException:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="module not found")


@router.put("/{module_id}", status_code=status.HTTP_200_OK)
async def update_module(module_id: uuid.UUID, update_module: ModuleUpdateRequest, module_service: Annotated[ModulesService, Depends(get_modules_service)],
                        current_user: UserRole = Depends(validate_token)):
    try:
        if current_user.role != Roles.ADMIN.value:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                                detail="This operation only allowed for admins")
        await module_service.update_module(module_id=module_id, update_module=update_module)
    except ModuleNotFoundException:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="No module found to update")


@router.post("/add", status_code=status.HTTP_200_OK)
async def add_module(module_add: ModuleInfo, module_service: Annotated[ModulesService, Depends(get_modules_service)],
                     current_user: UserRole = Depends(validate_token)) -> None:
    try:
        if current_user.role != Roles.ADMIN.value:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                                detail="This operation only allowed for admins")
        await module_service.add_module(add_module=module_add)
        return status.HTTP_201_CREATED
    except ModuleExistsException:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT,
                            detail="Module already exists")


@router.delete("/{module_name}", status_code=status.HTTP_200_OK)
async def delete_module(module_name: str, module_service: Annotated[ModulesService, Depends(get_modules_service)],
                        current_user: UserRole = Depends(validate_token)) -> None:

    if current_user.role != Roles.ADMIN.value:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail="This operation only allowed for admins")
    await module_service.delete_module(module_name=module_name)
    return status.HTTP_200_OK
