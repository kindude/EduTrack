import datetime
import uuid
from typing import List

from repositories.posts_repository import PostsRepository
from schemas.posts.post import Post
from schemas.posts.post_add_request import PostAddRequest
from schemas.posts.post_info import PostInfo


class PostsService:
    def __init__(self, posts_repo: PostsRepository):
        self.posts_repo = posts_repo

    async def get_posts_by_module(self, module_id: uuid.UUID) -> List[PostInfo]:
        return await self.posts_repo.get_posts_by_module_id(module_id)

    async def add_post(self, post_add: PostAddRequest):
        try:
            post = post_add.model_dump()
            post["id"] = uuid.uuid4()
            del post["date"]
            post["date"] = datetime.datetime.now()
            post = Post.model_validate(post)
            await self.posts_repo.add_post(post)
        except Exception as exc:
            print(exc)


    async def get_all_posts(self) -> List[PostInfo]:
        return await self.posts_repo.get_all_posts()
