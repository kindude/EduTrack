import uuid

from fastapi import APIRouter, Depends
from starlette import status

from api.dependencies import get_statistics_service
from services.statistics_service import StatisticsService

router = APIRouter()


@router.get('/average/{user_id}', status_code=status.HTTP_200_OK)
async def get_user_average(user_id: uuid.UUID, statistics_service: StatisticsService = Depends(get_statistics_service)) -> float:
    try:
        return await statistics_service.get_user_statistics(user_id)
    except:
        pass