"""

Модуль, предоставляющий базовую схему Pydantic с предварительно заданными настройками и определение поля SlugField.

Этот модуль предоставляет базовую схему Pydantic, настроенную с определенными конфигурационными параметрами,
а также определение SlugField для работы с текстовыми полями, представляющими URL-ссылки или слаги.

Содержит класс:
- BaseSchema: Базовая схема Pydantic с предварительно заданными настройками.

Содержит константу:
- SlugField: Строка Pydantic для работы с URL-ссылками или слагами.

Подробное описание атрибутов и константы смотрите в документации к классу BaseSchema и константе SlugField.

"""
from decimal import Decimal
from typing import Annotated

from pydantic import BaseModel, ConfigDict, constr, UrlConstraints, Field
from pydantic_core import Url


class BaseSchema(BaseModel):
    """

    Базовая схема Pydantic с предварительно заданными настройками.

        Attributes:
            model_config (ConfigDict): Настройки модели, включая допустимость
                произвольных типов (arbitrary_types_allowed) и создание модели из атрибутов класса (from_attributes).

    """

    model_config = ConfigDict(arbitrary_types_allowed=True, from_attributes=True)


SlugField = constr(min_length=2, max_length=30, pattern=r"^[a-zA-Z0-9-]+$", to_lower=True)

UrlField = Annotated[Url, UrlConstraints(max_length=255)]

DecimalField = Annotated[Decimal, Field(ge=0, default=0, decimal_places=2)]
