from sqlalchemy import Column, Integer, String, Boolean, DateTime, Index
from sqlalchemy.sql import func

from database.base import Base


class Link(Base):
    __tablename__ = "links"

    id = Column(Integer, primary_key=True, autoincrement=True, index=True)

    long_url = Column(String(2000), nullable=False, index=True)
    short_code = Column(String(64), unique=True, index=True, nullable=False)

    description = Column(String(500), nullable=True)
    is_active = Column(Boolean, nullable=False, default=True)
    click_count = Column(Integer, nullable=False, default=0)

    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)

    __table_args__ = (
        Index("idx_links_short_code_active", "short_code", "is_active"),
    )

    def __repr__(self) -> str:
        return f'<Link id={self.id} short_code={self.short_code!r}>'