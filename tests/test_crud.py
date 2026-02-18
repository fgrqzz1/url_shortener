"""
Тесты CRUD-операций для ссылок.
"""
import pytest

from app import crud
from app.schemas import LinkCreate
from models import Link


def test_create_short_link_generates_six_chars():
    """Короткий код должен состоять из 6 символов."""
    code = crud.create_short_link("https://example.com")
    assert len(code) == 6
    assert code.isalnum()


def test_create_short_link_different_for_same_url():
    """Разные вызовы должны генерировать разные коды (с высокой вероятностью)."""
    codes = {crud.create_short_link("https://example.com") for _ in range(10)}
    assert len(codes) > 1


def test_create_link(db_session):
    """Создание ссылки в БД."""
    link_in = LinkCreate(long_url="https://example.com", description="Тест")
    link = crud.create_link(db_session, link_in)
    assert link.id is not None
    assert link.short_code
    assert str(link.long_url) == "https://example.com/"
    assert link.description == "Тест"
    assert link.is_active is True
    assert link.click_count == 0


def test_get_link_by_short_code(db_session):
    """Поиск ссылки по короткому коду."""
    link_in = LinkCreate(long_url="https://test.com")
    created = crud.create_link(db_session, link_in)
    found = crud.get_link_by_short_code(db_session, created.short_code)
    assert found is not None
    assert found.id == created.id


def test_get_link_by_id(db_session):
    """Поиск ссылки по ID."""
    link_in = LinkCreate(long_url="https://id-test.com")
    created = crud.create_link(db_session, link_in)
    found = crud.get_link_by_id(db_session, created.id)
    assert found is not None
    assert found.id == created.id


def test_list_links(db_session):
    """Список ссылок возвращает созданные записи."""
    crud.create_link(db_session, LinkCreate(long_url="https://a.com"))
    crud.create_link(db_session, LinkCreate(long_url="https://b.com"))
    links = crud.list_links(db_session, limit=10)
    assert len(links) >= 2


def test_increment_click_count(db_session):
    """Увеличение счётчика кликов."""
    link_in = LinkCreate(long_url="https://clicks.com")
    link = crud.create_link(db_session, link_in)
    assert link.click_count == 0
    crud.increment_click_count(db_session, link)
    db_session.refresh(link)
    assert link.click_count == 1


def test_soft_delete_link(db_session):
    """Удаление ссылки из БД."""
    link_in = LinkCreate(long_url="https://delete-me.com")
    link = crud.create_link(db_session, link_in)
    link_id = link.id
    result = crud.soft_delete_link(db_session, link_id)
    assert result is not None
    found = crud.get_link_by_id(db_session, link_id)
    assert found is None
