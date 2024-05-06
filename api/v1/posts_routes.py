import uuid
from typing import List, Union

from fastapi import APIRouter, Depends
from starlette import status

from api.dependencies import get_posts_service
from schemas.posts.post_add_request import PostAddRequest
from schemas.posts.post_info import PostInfo
from services.posts_service import PostsService

router = APIRouter()


@router.post('/add', status_code=status.HTTP_201_CREATED)
async def add_post(post_add: PostAddRequest, posts_service: PostsService = Depends(get_posts_service)):
    try:
        await posts_service.add_post(post_add)
        return status.HTTP_201_CREATED
    except:
        pass

@router.get('/{module_id}/feed', status_code=status.HTTP_200_OK)
async def get_posts(module_id: uuid.UUID, posts_service: PostsService = Depends(get_posts_service)) -> Union[List[PostInfo]]:
    try:
        return await posts_service.get_posts_by_module(module_id)
    except:
        pass


@router.get('/all', status_code=status.HTTP_200_OK)
async def get_all_posts(posts_service: PostsService = Depends(get_posts_service)):
    try:
        return await posts_service.get_all_posts()
    except:
        pass
