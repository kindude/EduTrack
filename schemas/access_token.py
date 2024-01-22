"""
Модуль для работы с моделью токена.

Этот модуль предоставляет модель для отображения токена, включая значение токена доступа и его тип.
"""
from schemas.base import BaseSchema


class AccessToken(BaseSchema):
    """
    Модель токена.

    Attributes:
        token: Значение токена доступа.
        type: Тип токена.
    """

    token: str
    type: str
