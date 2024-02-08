from datetime import datetime
from typing import List
from uuid import UUID

from sqlalchemy import Float, DateTime, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from models.attendance import AttendanceDao
from models.type_of_mark import TypeOfMarkDao
from models.base import BaseModel


class DayDao(BaseModel):
    __tablename__ = 'days'

    id: Mapped[UUID] = mapped_column(primary_key=True)
    presence_id: Mapped[UUID] = mapped_column(ForeignKey('attendance.id'))
    type_of_mark_id: Mapped[UUID] = mapped_column(ForeignKey('type_of_mark.id'))
    mark: Mapped[float] = mapped_column(Float, nullable=True)
    date: Mapped[datetime] = mapped_column(DateTime, nullable=False)
    user_id: Mapped[UUID] = mapped_column(ForeignKey('users.id'))
    module_id: Mapped[UUID] = mapped_column(ForeignKey('modules.id'))

    user: Mapped["UserDao"] = relationship(back_populates='days')
    module: Mapped["ModuleDao"] = relationship(back_populates='days')

    presence: Mapped["AttendanceDao"] = relationship(back_populates='day')
    type_of_mark: Mapped["TypeOfMarkDao"] = relationship(back_populates='day')

    comments: Mapped[List["CommentDao"]] = relationship(back_populates='day')
