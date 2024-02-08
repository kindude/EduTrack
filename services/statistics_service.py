import math
import uuid
from itertools import count

from repositories.actions_repo import ActionsRepository
from repositories.days_repository import DaysRepository


class StatisticsService:

    def __init__(self, days_repo: DaysRepository):
        self.days_repo = days_repo

    async def get_user_statistics(self, user_id: uuid.UUID) -> float:
        users_marks = await self.days_repo.get_days_by_user_id(user_id)
        user_marks = users_marks[0]
        days_count = 0
        total = 0
        for day in user_marks.days:
            if day.mark is not None:
                total += day.mark
                days_count += 1

        average = round(float(total / days_count), 2)

        return average
