"""
Тесты утилит для работы с URL.
"""
import pytest

from app.utils.url_helpers import (
    normalize_url,
    is_valid_short_code,
    truncate_url,
    extract_domain,
)


def test_normalize_url_adds_https():
    """URL без схемы получает https://."""
    assert normalize_url("example.com") == "https://example.com"


def test_normalize_url_preserves_https():
    """URL с https остаётся без изменений."""
    assert normalize_url("https://example.com") == "https://example.com"


def test_normalize_url_strips_whitespace():
    """Пробелы в начале и конце убираются."""
    assert normalize_url("  https://example.com  ") == "https://example.com"


def test_normalize_url_empty_returns_empty():
    """Пустая строка возвращает пустую строку."""
    assert normalize_url("") == ""


def test_is_valid_short_code_valid():
    """Корректный короткий код из 6 символов."""
    assert is_valid_short_code("abc123") is True
    assert is_valid_short_code("AbCdEf") is True
    assert is_valid_short_code("123456") is True


def test_is_valid_short_code_invalid_length():
    """Неверная длина кода."""
    assert is_valid_short_code("abc12") is False
    assert is_valid_short_code("abc1234") is False
    assert is_valid_short_code("") is False


def test_is_valid_short_code_invalid_chars():
    """Недопустимые символы в коде."""
    assert is_valid_short_code("abc-12") is False
    assert is_valid_short_code("abc 12") is False


def test_truncate_url_short():
    """Короткий URL не обрезается."""
    url = "https://short.com"
    assert truncate_url(url, max_length=80) == url


def test_truncate_url_long():
    """Длинный URL обрезается с многоточием."""
    url = "https://" + "a" * 100
    result = truncate_url(url, max_length=30)
    assert len(result) == 30
    assert result.endswith("...")


def test_extract_domain():
    """Извлечение домена из URL."""
    assert extract_domain("https://example.com/path") == "example.com"
    assert extract_domain("http://sub.domain.org") == "sub.domain.org"


def test_extract_domain_empty():
    """Пустой или невалидный URL."""
    assert extract_domain("") == ""
