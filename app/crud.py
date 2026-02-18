from typing import Optional
import secrets

from sqlalchemy.orm import Session
from sqlalchemy import select

import models
from app.schemas import LinkCreate


def increment_click_count(db: Session, link: models.Link) -> None:
    link.click_count += 1
    db.add(link)
    db.commit()
    db.refresh(link)

def create_short_link(long_url: str) -> str:
    alphabet = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"
    return "".join(secrets.choice(alphabet) for _ in range(6))

def create_link(db: Session, link_in: LinkCreate) -> models.Link:
    short_code = create_short_link(link_in.long_url)

    db_link = models.Link(
        long_url = str(link_in.long_url),
        short_code=short_code,
        description=link_in.description,
    )
    db.add(db_link)
    db.commit
    db.refresh(db_link)
    

    return db_link
