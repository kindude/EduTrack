from datetime import datetime
from uuid import UUID

from sqlalchemy import Boolean, Float, DateTime, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from models.base import BaseModel


class DayDao(BaseModel):

    __tablename__ = 'days'

    id: Mapped[UUID] = mapped_column(primary_key=True)
    presence: Mapped[bool] = mapped_column(Boolean, nullable=False)
    mark: Mapped[float] = mapped_column(Float, nullable=True)
    date: Mapped[datetime] = mapped_column(DateTime, nullable=False)
    user_id: Mapped[UUID] = mapped_column(ForeignKey('users.id'))
    module_id: Mapped[UUID] = mapped_column(ForeignKey('modules.id'))

    user: Mapped["UserDao"] = relationship(back_populates='days')
    module: Mapped["ModuleDao"] = relationship(back_populates='days')
