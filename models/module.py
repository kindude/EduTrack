import uuid
from typing import List
from uuid import UUID

from sqlalchemy import String, Integer, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from models.base import BaseModel


class ModuleDao(BaseModel):

    __tablename__ = "modules"

    id: Mapped[UUID] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String(100))
    alias: Mapped[str] = mapped_column(String(20))
    hours_taught: Mapped[int] = mapped_column(Integer, nullable=False)

    actions: Mapped[List["ActionDao"]] = relationship(back_populates="module")
    days: Mapped[List["DayDao"]] = relationship(back_populates='module')
    posts: Mapped[List["PostDao"]] = relationship(back_populates='module')

