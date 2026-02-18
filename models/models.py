from pickle import TRUE
from time import timezone
from sqlalchemy import Column, Integer, String, Boolean, DateTime, Index, true
from sqlalchemy.sql import func

from database.base import Base


class Link(Base):
    __tablename__ = "links"

    id = Column(Integer, primary_key=True, autoincrement=True)

    long_url = Column(String(2000), nullabele=False, index=True)
    short_url = Column(String(64), unique=True, index=True)

    description = Column(String(500), nullabel=True)
    is_active = Column(Boolean, nullable=False, default=True)
    click_count = Column(Integer, nullable=False, default=0)

    created_at = Column(DataTime(timezone=True), server_default=func.now(), nullable=False)

    __table_args__ = (Index("idx_links_short_code_active", "short_code", "is_active"))

    def __repr__(self) -> str:
        return f'<Link id={self.id} short_code={self.short_code!r}>'