"""
Модуль `main.py` представляет точку входа для запуска FastAPI-приложения.

Содержит код для создания и конфигурации FastAPI-приложения, включая подключение API маршрутов,
настройку Swagger UI и запуск приложения.

Attributes:
    settings (ServerSettings): Объект настроек сервера
    app (FastAPI): FastAPI-приложение.
"""

import uvicorn
from fastapi import FastAPI
from api.api import api_routers
from settings import ServerSettings

settings = ServerSettings()
app = FastAPI()

for api_router in api_routers:
    app.include_router(api_router, prefix="/api")

if not settings.debug_mode:
    app.swagger_ui_init_oauth = None
    app.openapi_url = ""
    app.docs_url = ""
    app.redoc_url = ""


if __name__ == "__main__":
    uvicorn.run("main:app", host='0.0.0.0', port=settings.port, reload=True)
