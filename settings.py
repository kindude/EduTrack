"""
Модуль `settings.py` представляет собой файл с настройками приложения.

Содержит настройки, такие как порт, хост, секретные ключи для генерации
    токенов доступа и обновления, время их истечения, соль для хеширования паролей и режим отладки.
"""


from dotenv import load_dotenv
from pydantic import PostgresDsn, RedisDsn, Field
from pydantic_settings import BaseSettings

load_dotenv()


class ServerSettings(BaseSettings):
    """
    Представляет настройки сервера

    Attributes:
        port (str): Порт, на котором будет запущено приложение.
        debug_mode (bool): Режим отладки (True - включен, False - выключен).
    """
    port: int = Field(alias='app_port')
    debug_mode: bool = False


class DatabaseSettings(BaseSettings):
    """
    Представляет настройки к БД

    Attributes:
        postgres_url (PostgresDsn): Строка подключения к PostgreSQL
        redis_url (RedisDsn): Строка подключения к Redis
    """

    postgres_url: PostgresDsn
    redis_url: RedisDsn


class JwtSettings(BaseSettings):
    """
    Представляет настройки JWT

    Attributes:
        access_secret_key (str): Секретный ключ для генерации токенов доступа.
        access_expiration (int): Время истечения токенов доступа в секундах.
        refresh_secret_key (str): Секретный ключ для генерации токенов обновления.
        refresh_expiration (int): Время истечения токенов обновления в секундах.
    """

    access_secret_key: str
    access_expiration: int
    refresh_secret_key: str
    refresh_expiration: int


class PasswordSettings(BaseSettings):
    """
    Представляет настройки паролей

    Attributes:
        password_salt (str): Соль для хеширования паролей.
    """

    password_salt: str = Field(alias='salt_password')


class AppSettings(BaseSettings):

    artificial_password: str
