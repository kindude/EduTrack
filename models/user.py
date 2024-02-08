import enum
import uuid
from typing import List
from uuid import UUID

from sqlalchemy import String, Enum, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from models.comment import CommentDao
from models.base import BaseModel


class Roles(enum.Enum):
    STUDENT = "STUDENT"
    TEACHER = "TEACHER"
    ADMIN = "ADMIN"
    MODERATOR = "MODERATOR"




class UserDao(BaseModel):
    __tablename__ = "users"

    id: Mapped[UUID] = mapped_column(primary_key=True)
    first_name: Mapped[str] = mapped_column(String(50))
    last_name: Mapped[str] = mapped_column(String(50))
    phone_number: Mapped[str] = mapped_column(String(20), unique=True)
    city: Mapped[str] = mapped_column(String(50))
    address: Mapped[str] = mapped_column(String(150))
    email: Mapped[str] = mapped_column(String(100), unique=True)
    password_hash: Mapped[str] = mapped_column(String(300))
    role: Mapped[Enum] = mapped_column(Enum(Roles))
    image_id: Mapped[uuid.UUID] = mapped_column(ForeignKey('images.id'), nullable=True)

    actions: Mapped[List["ActionDao"]] = relationship(
        "ActionDao", back_populates="user", cascade="all, delete-orphan"
    )
    days: Mapped[List["DayDao"]] = relationship(
        "DayDao", back_populates="user", cascade="all, delete-orphan"
    )
    posts: Mapped[List["PostDao"]] = relationship(
        "PostDao", back_populates="author", cascade="all, delete-orphan"
    )
    image: Mapped["ImageDao"] = relationship(
        "ImageDao", back_populates="user", cascade="all, delete-orphan", single_parent=True
    )

    comments: Mapped["CommentDao"] = relationship(
        back_populates='author'
    )

