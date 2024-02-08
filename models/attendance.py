import enum
import uuid
from typing import List

from sqlalchemy import Enum
from sqlalchemy.orm import Mapped, mapped_column, relationship

from models.base import BaseModel


class AttendanceTypes(enum.Enum):
    ABSENT = "ABSENT"
    PRESENT = "PRESENT"


class AttendanceDao(BaseModel):
    __tablename__ = 'attendance'

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True)
    type: Mapped[enum.Enum] = mapped_column(Enum(AttendanceTypes))

    day: Mapped["DayDao"] = relationship(back_populates='presence')
