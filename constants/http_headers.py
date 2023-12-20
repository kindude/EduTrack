"""
Модуль HttpHeaders

Этот модуль содержит класс HttpHeaders для предоставления HTTP заголовков.

Classes:
    - HttpHeaders: Класс для предоставления HTTP заголовков.

Attributes:
    - WWW_AUTHENTICATE_BEARER: Словарь с заголовком WWW-Authenticate
            для аутентификации по схеме Bearer.
"""


class HttpHeaders:
    """
    Класс HttpHeaders для предоставления HTTP заголовков.

    Attributes:
        - WWW_AUTHENTICATE_BEARER (dict): Словарь с заголовком WWW-Authenticate
                для аутентификации по схеме Bearer.
    """
    WWW_AUTHENTICATE_BEARER = {"WWW-Authenticate": "Bearer"}
