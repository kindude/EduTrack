"""
Модуль PasswordHelper

Этот модуль предоставляет класс `PasswordHelper` для хэширования и проверки паролей
с использованием соли.

Классы:
    PasswordHelper: Утилита для хэширования и проверки паролей с использованием соли.

Constants:
    - settings: Объект настроек паролей
"""

import hashlib

from settings import PasswordSettings

settings = PasswordSettings()


class PasswordHelper:
    """
    Инициализирует объект PasswordHelper с заданным значением соли.

    Attributes:
        salt (str): Строка соль для хэширования паролей.
    """

    def __init__(self):
        self.salt = settings.password_salt

    def hash_password(self, password: str) -> str:
        """
        Хэширует переданный пароль с использованием соли.

        Args:
            password (str): Пароль для хэширования.

        Returns:
            str: Хэш-значение пароля.
        """

        password_hash = str(password) + self.salt
        hashed = hashlib.sha256(password_hash.encode()).hexdigest()
        return hashed

    def check_password(self, login_password: str, password: str) -> bool:
        """
        Проверяет соответствие хэш-значения пароля и хэш-значения входа.

        Args:
            login_password (str): Введенный пользователем пароль.
            password (str): Хэш-значение пароля для сравнения.

        Returns:
            bool: True, если хэш-значения совпадают, иначе False.
        """

        return self.hash_password(password=login_password) == password
