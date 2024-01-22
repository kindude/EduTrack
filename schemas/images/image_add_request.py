import uuid

from pydantic import Field

from schemas.base import BaseSchema


class ImageAddRequest(BaseSchema):
    id: uuid.UUID
    name: str
    image_data: bytes = Field(..., description="Binary image data")
