import uuid
from typing import List

from sqlalchemy import select
from sqlalchemy.orm import selectinload

from models.post import PostDao
from repositories.base import BaseRepository
from schemas.modules.module_info import ModuleInfo
from schemas.posts.post import Post
from schemas.posts.post_info import PostInfo
from schemas.users.user import UserInfo


class PostsRepository(BaseRepository):

    model = PostDao

    async def add_post(self, post: Post) -> None:
        await self._add(post.model_dump())

    async def get_posts_by_module_id(self, module_id: uuid.UUID) -> List[PostInfo]:
        stmt_to_select_posts = select(self.model).filter(self.model.module_id == module_id).options(
            selectinload(self.model.module),
            selectinload(self.model.author)
        )
        posts = await self.session.execute(stmt_to_select_posts)
        posts = posts.scalars().all()
        posts_info = []
        for post in posts:
            author = UserInfo.model_validate(post.author)
            module = ModuleInfo.model_validate(post.module)

            posts_info.append(
                PostInfo(
                    id=post.id,
                    title=post.title,
                    text=post.text,
                    date=post.date,
                    author=author,
                    module=module
                )
            )
        return posts_info

    async def get_all_posts(self) -> List[PostInfo]:
        stmt_to_select_posts = select(self.model).options(
            selectinload(self.model.module),
            selectinload(self.model.author)
        )
        posts = await self.session.execute(stmt_to_select_posts)
        posts = posts.scalars().all()
        posts_info = []
        for post in posts:
            author = UserInfo.model_validate(post.author)
            module = ModuleInfo.model_validate(post.module)

            posts_info.append(
                PostInfo(
                    id=post.id,
                    title=post.title,
                    text=post.text,
                    date=post.date,
                    author=author,
                    module=module
                )
            )
        return posts_info

