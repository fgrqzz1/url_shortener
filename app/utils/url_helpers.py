"""
Вспомогательные функции для работы с URL и короткими кодами.
"""
import re
from urllib.parse import urlparse


def normalize_url(url: str) -> str:
    """
    Нормализует URL: добавляет схему при необходимости, убирает лишние пробелы.
    """
    url = url.strip()
    if not url:
        return ""
    parsed = urlparse(url)
    if not parsed.scheme:
        return f"https://{url}"
    return url


def is_valid_short_code(code: str, length: int = 6) -> bool:
    """
    Проверяет, что короткий код соответствует ожидаемому формату:
    только буквы и цифры, заданной длины.
    """
    if not code or len(code) != length:
        return False
    pattern = re.compile(r"^[a-zA-Z0-9]+$")
    return bool(pattern.match(code))


def truncate_url(url: str, max_length: int = 80) -> str:
    """
    Обрезает длинный URL для отображения, добавляя многоточие.
    """
    if len(url) <= max_length:
        return url
    return url[: max_length - 3] + "..."


def extract_domain(url: str) -> str:
    """
    Извлекает домен из URL для отображения или логирования.
    """
    try:
        parsed = urlparse(url)
        return parsed.netloc or ""
    except Exception:
        return ""
