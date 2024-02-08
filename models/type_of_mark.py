import enum
import uuid
from typing import List

from sqlalchemy import Enum
from sqlalchemy.orm import Mapped, mapped_column, relationship

from models.base import BaseModel


class MarkTypes(enum.Enum):
    LABMARK = 'LABMARK'
    COURSEWORK = 'COURSEWORK'


class TypeOfMarkDao(BaseModel):
    __tablename__ = 'type_of_mark'

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True)
    type_of_mark: Mapped[enum.Enum] = mapped_column(Enum(MarkTypes))

    day: Mapped["DayDao"] = relationship(back_populates='type_of_mark')

