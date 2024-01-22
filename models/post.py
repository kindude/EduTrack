import datetime
import uuid

from sqlalchemy import ForeignKey, String, DateTime
from sqlalchemy.orm import Mapped, mapped_column, relationship

from models.base import BaseModel


class PostDao(BaseModel):

    __tablename__ = 'posts'

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String(50))
    text: Mapped[str] = mapped_column(String(500))
    date: Mapped[datetime.datetime] = mapped_column(DateTime())
    author_id: Mapped[uuid.UUID] = mapped_column(ForeignKey('users.id'))
    module_id: Mapped[uuid.UUID] = mapped_column(ForeignKey('modules.id'))

    author: Mapped["UserDao"] = relationship(back_populates="posts")
    module: Mapped["ModuleDao"] = relationship(back_populates="posts")
