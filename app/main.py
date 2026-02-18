from fastapi import FastAPI

from config.config import config
from app.database import Base, engine
from app.routers import shortener

def create_app() -> FastAPI:
    app = FastAPI(
        titile=config.app_name,
        debug=config.debug,
        version=str(config.version)
    )

    app.include_router(shortener.router)

    @app.get('/health', tags=['system'])
    def health_check():
        return {'status': 'ok'}
    return app

app = create_app()