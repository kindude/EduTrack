from models.image import ImageDao
from repositories.base import BaseRepository
from schemas.images.image_add_request import ImageAddRequest


class ImagesRepository(BaseRepository):

    model = ImageDao

    async def add_image(self, image_add: ImageAddRequest):
        await self._add(image_add.model_dump())
