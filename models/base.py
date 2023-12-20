"""
Модуль BaseModel

Этот модуль предоставляет базовую модель для SQLAlchemy моделей.

Classes:
    BaseModel: Базовая модель для SQLAlchemy моделей.

Attributes:
    Base: Объект, представляющий базовую модель SQLAlchemy.
"""

from sqlalchemy.orm import declarative_base

Base = declarative_base()


class BaseModel(Base):
    """
    Базовая модель для SQLAlchemy моделей.
    """

    __abstract__ = True
