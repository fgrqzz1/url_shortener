from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

from config.config import config


Base = declarative_base()


engine = create_engine(
    config.database_url,
    echo=config.debug,
    future=True,
    connect_args={"check_same_thread": False} if config.database_engine == "sqlite3" else {}, 
)

SessionLocal = sessionmaker(
    bind=engine,
    autoflush=False,
    autocommit=False,
    future=True,
)
