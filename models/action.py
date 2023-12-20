import uuid

from sqlalchemy import ForeignKey, Enum
from sqlalchemy.orm import mapped_column, Mapped, relationship

from models.base import BaseModel
from models.user import Roles


class ActionDao(BaseModel):

    __tablename__ = "actions"

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True)
    user_id: Mapped[uuid.UUID] = mapped_column(ForeignKey('users.id'))
    module_id: Mapped[uuid.UUID] = mapped_column(ForeignKey('modules.id'))
    role: Mapped[Enum] = mapped_column(Enum(Roles))

    module: Mapped["ModuleDao"] = relationship(back_populates="actions")
    user: Mapped["UserDao"] = relationship(back_populates="actions")
