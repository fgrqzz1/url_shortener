from pathlib import Path

from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.responses import FileResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles

from config.config import config
from database import Base, engine, get_db
from app.routers import shortener
from app import crud


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

    @app.get("/{short_code}", include_in_schema=False)
    def redirect_short_code(short_code: str, db=Depends(get_db)):
        link = crud.get_link_by_short_code(db, short_code)
        if not link:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Link not found",
            )

        crud.increment_click_count(db, link)
        return RedirectResponse(url=link.long_url, status_code=status.HTTP_307_TEMPORARY_REDIRECT)

    return app


app = create_app()

# Создание таблиц БД (временно, потом перенесём в Alembic)
Base.metadata.create_all(bind=engine)