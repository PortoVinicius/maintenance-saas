from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from app.core.config import settings
from app.api.web.dashboard import router


def create_app() -> FastAPI:
    app = FastAPI(
        title=settings.app_name,
        debug=settings.debug
    )

    # Arquivos estáticos (CSS, JS, imagens)
    app.mount(
        "/static",
        StaticFiles(directory="app/static"),
        name="static"
    )

    app.include_router(router)

    return app


app = create_app()
