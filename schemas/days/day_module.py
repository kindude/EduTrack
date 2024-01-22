
from schemas.base import BaseSchema
from schemas.days.day_info import DayInfo
from schemas.modules.module_info import ModuleInfo


class DayModule(BaseSchema):
    day: DayInfo
    module: ModuleInfo
