import uuid

from repositories.actions_repo import ActionsRepository
from schemas.actions.action import Action
from schemas.actions.action_add_request import ActionAddRequest


class ActionsService:

    def __init__(self, actions_repo: ActionsRepository):

        self.actions_repo = actions_repo

    async def enroll_user(self, action_add: ActionAddRequest) -> None:

        action = Action(
            id=uuid.uuid4(),
            user_id=action_add.user_id,
            module_id=action_add.module_id,
            role=action_add.role
        )
        await self.actions_repo.add_action(action)

    async def get_users(self, module_id: uuid.UUID):
        await self.actions_repo.get_users_by_module_id(module_id)

    async def get_modules(self, user_id: uuid.UUID):
        await self.actions_repo.get_modules_by_user_id(user_id)

    def delete_user(self):
        pass
