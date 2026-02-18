"""
Валидаторы для URL Shortener.
"""
import re
from typing import Optional


def validate_short_code(code: str, min_len: int = 4, max_len: int = 32) -> Optional[str]:
    """
    Проверяет короткий код на корректность.
    Возвращает сообщение об ошибке или None при успехе.
    """
    if not code:
        return "Код не может быть пустым"
    if len(code) < min_len:
        return f"Код должен быть не короче {min_len} символов"
    if len(code) > max_len:
        return f"Код должен быть не длиннее {max_len} символов"
    if not re.match(r"^[a-zA-Z0-9_-]+$", code):
        return "Код может содержать только буквы, цифры, дефис и подчёркивание"
    return None


def validate_description(description: Optional[str], max_length: int = 500) -> Optional[str]:
    """
    Проверяет описание ссылки.
    Возвращает сообщение об ошибке или None при успехе.
    """
    if description is None:
        return None
    if len(description) > max_length:
        return f"Описание не должно превышать {max_length} символов"
    return None


def sanitize_description(description: Optional[str]) -> Optional[str]:
    """
    Очищает описание от лишних пробелов по краям.
    Пустая строка после очистки возвращается как None.
    """
    if description is None:
        return None
    cleaned = description.strip()
    return cleaned if cleaned else None
