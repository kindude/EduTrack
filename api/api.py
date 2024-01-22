"""
Модуль api.py содержит конфигурацию и настройку API-маршрутов для приложения.

Этот модуль отвечает за создание маршрутов и подключение обработчиков для версии API v1.
"""

from fastapi import APIRouter
from api.v1 import users, auth, modules, action_routes, statistics_routes, posts_routes

api_v1_router = APIRouter(prefix="/v1")
api_v1_router.include_router(users.router, prefix="/users", tags=["Users"])
api_v1_router.include_router(auth.router, prefix="/auth", tags=["Auth"])
api_v1_router.include_router(modules.router, prefix="/modules", tags=["Modules"])
api_v1_router.include_router(action_routes.router, prefix="/actions", tags=["Actions"])
api_v1_router.include_router(statistics_routes.router, prefix="/statistics", tags=["Statistics"])
api_v1_router.include_router(posts_routes.router, prefix="/posts", tags=["Posts"])
api_routers = [api_v1_router]
