"""
Тесты валидаторов URL Shortener.
"""
import pytest

from app.validators import (
    validate_short_code,
    validate_description,
    sanitize_description,
)


def test_validate_short_code_valid():
    """Корректные коды проходят валидацию."""
    assert validate_short_code("abc123") is None
    assert validate_short_code("AbC-123") is None
    assert validate_short_code("x_y_z") is None


def test_validate_short_code_empty():
    """Пустой код не проходит."""
    assert validate_short_code("") is not None


def test_validate_short_code_too_short():
    """Слишком короткий код."""
    assert validate_short_code("ab", min_len=4) is not None


def test_validate_short_code_too_long():
    """Слишком длинный код."""
    assert validate_short_code("a" * 40, max_len=32) is not None


def test_validate_short_code_invalid_chars():
    """Недопустимые символы."""
    assert validate_short_code("abc!@#") is not None
    assert validate_short_code("abc 123") is not None


def test_validate_description_none():
    """None — допустимое описание."""
    assert validate_description(None) is None


def test_validate_description_short():
    """Короткое описание проходит."""
    assert validate_description("Краткое") is None


def test_validate_description_too_long():
    """Слишком длинное описание."""
    long_desc = "x" * 501
    assert validate_description(long_desc) is not None


def test_sanitize_description_none():
    """None остаётся None."""
    assert sanitize_description(None) is None


def test_sanitize_description_strips():
    """Пробелы убираются."""
    assert sanitize_description("  текст  ") == "текст"


def test_sanitize_description_empty_becomes_none():
    """Пустая строка после очистки становится None."""
    assert sanitize_description("   ") is None
