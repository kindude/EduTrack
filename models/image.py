import uuid

from sqlalchemy import String, LargeBinary, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from models.base import BaseModel


class ImageDao(BaseModel):

    __tablename__ = "images"

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(50))
    image_data: Mapped[bytes] = mapped_column(LargeBinary)

    user: Mapped["UserDao"] = relationship(back_populates='image')

