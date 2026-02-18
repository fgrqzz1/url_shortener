from pathlib import Path

from fastapi import FastAPI
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles

from config.config import config
from database import Base, engine
from app.routers import shortener


BASE_DIR = Path(__file__).resolve().parent.parent
STATIC_DIR = BASE_DIR / "static"


def create_app() -> FastAPI:
    app = FastAPI(
        title=config.app_name,
        debug=config.debug,
        version=str(config.version),
    )

    app.include_router(shortener.router)

    @app.get("/health", tags=["system"])
    def health_check():
        return {"status": "ok"}

    # Статика и главная страница
    app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")

    @app.get("/", include_in_schema=False)
    def landing_page():
        return FileResponse(STATIC_DIR / "index.html")

    return app


app = create_app()

# Создание таблиц БД (временно, потом перенесём в Alembic)
Base.metadata.create_all(bind=engine)