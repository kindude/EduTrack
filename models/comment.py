from uuid import UUID

from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from models.base import BaseModel


class CommentDao(BaseModel):

    __tablename__ = 'comments'

    id: Mapped[UUID] = mapped_column(primary_key=True)

    author_id: Mapped[UUID] = mapped_column(ForeignKey('users.id'))
    day_id: Mapped[UUID] = mapped_column(ForeignKey('days.id'))
    text: Mapped[str] = mapped_column(String)

    day: Mapped["DayDao"] = relationship(back_populates='comments')
    author: Mapped["UserDao"] = relationship(back_populates='comments')
