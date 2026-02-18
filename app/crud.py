from typing import Optional, List
import secrets

from sqlalchemy.orm import Session
from sqlalchemy import select

from models import Link
from app.schemas import LinkCreate


def get_link_by_short_code(db: Session, short_code: str) -> Optional[Link]:
    stmt = select(Link).where(
        Link.short_code == short_code,
        Link.is_active.is_(True),
    )
    return db.execute(stmt).scalar_one_or_none()


def increment_click_count(db: Session, link: Link) -> None:
    link.click_count += 1
    db.add(link)
    db.commit()
    db.refresh(link)


def create_short_link(long_url: str) -> str:
    alphabet = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"
    return "".join(secrets.choice(alphabet) for _ in range(6))


def create_link(db: Session, link_in: LinkCreate) -> Link:
    short_code = create_short_link(link_in.long_url)

    db_link = Link(
        long_url=str(link_in.long_url),
        short_code=short_code,
        description=link_in.description,
    )
    db.add(db_link)
    db.commit()
    db.refresh(db_link)
    
    return db_link

def list_links(db: Session, limit: int = 100, offset = 0) -> list[Link]:
    stmt = (
        select(Link).order_by(Link.id_desc()).limit(limit).offset(offset)
    )
    result = db.execute(stmt)
    
    return list(result.scalars().all())

def soft_delete_link(db: Session, short_code: str) -> Optional[Link]:
    link = get_link_by_short_code(db, short_code)
    if not link:
        return None

    link.is_active = False
    db.add(link)
    db.commit()
    db.refresh(link)

    return link
