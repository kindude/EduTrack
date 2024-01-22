from typing import List, Union

from schemas.base import BaseSchema
from schemas.modules.module_info import ModuleInfo
from schemas.users.user import UserInfo


class ModuleUsers(BaseSchema):
    module: ModuleInfo
    users: Union[List[UserInfo], str]
