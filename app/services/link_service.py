"""
Сервис для работы со ссылками: бизнес-логика поверх CRUD.
"""
from typing import Optional

from sqlalchemy.orm import Session

from models import Link
from app import crud
from app.schemas import LinkCreate
from app.utils import is_valid_short_code


class LinkService:
    """Сервис управления ссылками."""

    def __init__(self, db: Session):
        self.db = db

    def create(self, link_in: LinkCreate) -> Link:
        """Создаёт новую короткую ссылку."""
        return crud.create_link(self.db, link_in)

    def get_by_id(self, link_id: int) -> Optional[Link]:
        """Возвращает ссылку по ID."""
        return crud.get_link_by_id(self.db, link_id)

    def get_by_short_code(self, short_code: str) -> Optional[Link]:
        """Возвращает ссылку по короткому коду."""
        if not is_valid_short_code(short_code):
            return None
        return crud.get_link_by_short_code(self.db, short_code)

    def list(self, limit: int = 100, offset: int = 0) -> list[Link]:
        """Возвращает список ссылок с пагинацией."""
        return crud.list_links(self.db, limit=limit, offset=offset)

    def delete(self, link_id: int) -> Optional[Link]:
        """Удаляет ссылку из БД."""
        return crud.soft_delete_link(self.db, link_id)

    def record_click(self, link: Link) -> None:
        """Увеличивает счётчик кликов по ссылке."""
        crud.increment_click_count(self.db, link)
