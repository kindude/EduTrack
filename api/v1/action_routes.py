import uuid
from typing import Annotated

from fastapi import APIRouter, Depends
from starlette import status

from api.dependencies import get_actions_service, get_days_service
from schemas.actions.action_add_request import ActionAddRequest
from schemas.days.day_add_request import DayAddRequest
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
                           actions_service: Annotated[ActionsService, Depends(get_actions_service)]):
    try:
        await actions_service.get_users(module_id)
    except:
        pass

@router.get('/user/{user_id}/modules', status_code=status.HTTP_200_OK)
async def get_user_modules(user_id: uuid.UUID,
                           actions_service: Annotated[ActionsService, Depends(get_actions_service)]):
    try:
        await actions_service.get_modules(user_id)
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
async def get_user_days(id: uuid.UUID, days_service: Annotated[DaysService, Depends(get_days_service)]):
    try:
        await days_service.get_days_by_user(id)
    except:
        pass
