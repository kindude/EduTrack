import datetime
import uuid

from pydantic import constr

from schemas.base import BaseSchema


class Post(BaseSchema):
    id: uuid.UUID
    title: constr(min_length=2)
    text: constr(min_length=2)
    date: datetime.datetime
    author_id: uuid.UUID
    module_id: uuid.UUID
