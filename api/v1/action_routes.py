import uuid
from typing import Annotated, List

from fastapi import APIRouter, Depends
from starlette import status

from api.dependencies import get_actions_service, get_days_service
from api.dependencies_user import get_current_user
from schemas.actions.action_add_request import ActionAddRequest
from schemas.days.day_add_request import DayAddRequest
from schemas.days.day_module import DayModule
from schemas.modules.module_users import ModuleUsers
from schemas.users.user import UserInfo
from schemas.users.user_marks import UserMarks
from services.actions_service import ActionsService
from services.days_service import DaysService

router = APIRouter()


@router.post('/add', status_code=status.HTTP_201_CREATED)
async def enroll_user(action: ActionAddRequest,
                      actions_service: Annotated[ActionsService, Depends(get_actions_service)]):

    try:
        await actions_service.enroll_user(action)
        return status.HTTP_201_CREATED
    except:
        pass


@router.get('/module/{module_id}/users', status_code=status.HTTP_200_OK)
async def get_module_users(module_id: uuid.UUID,
                           actions_service: Annotated[ActionsService, Depends(get_actions_service)]) -> ModuleUsers:
    try:
        return await actions_service.get_users(module_id)
    except:
        pass


@router.get('/user/modules', status_code=status.HTTP_200_OK)
async def get_user_modules(actions_service: Annotated[ActionsService, Depends(get_actions_service)],
                           current_user: UserInfo = Depends(get_current_user)):
    try:
        return await actions_service.get_modules(current_user.id)
    except:
        pass


@router.post('/mark', status_code=status.HTTP_201_CREATED)
async def add_day(day: DayAddRequest, days_service: Annotated[DaysService, Depends(get_days_service)]):
    try:
        await days_service.add_day(day)
    except:
        pass


@router.get('/module/{id}/marks', status_code=status.HTTP_200_OK)
async def get_module_days(id: uuid.UUID, days_service: Annotated[DaysService, Depends(get_days_service)]):
    try:
        await days_service.get_days_by_module(id)
    except:
        pass


@router.get('/user/{id}/marks', status_code=status.HTTP_200_OK)
async def get_user_days(id: uuid.UUID, days_service: Annotated[DaysService, Depends(get_days_service)]) -> List[UserMarks]:
    try:
        return await days_service.get_days_by_user(id)
    except:
        pass


@router.get('/users/marks', status_code=status.HTTP_200_OK)
async def get_users_days(days_service: Annotated[DaysService, Depends(get_days_service)]) -> List[UserMarks]:
    try:
        return await days_service.get_days_users()
    except:
        pass

@router.get('/users/marks/{teacher_id}', status_code=status.HTTP_200_OK)
async def get_users_days_by_teacher_id(teacher_id: uuid.UUID, days_service: Annotated[DaysService, Depends(get_days_service)]) -> List[UserMarks]:
    try:
        return await days_service.get_days_by_teacher(teacher_id=teacher_id)
    except:
        pass