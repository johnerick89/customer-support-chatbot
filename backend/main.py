from collections.abc import AsyncIterator
from contextlib import asynccontextmanager

from fastapi import FastAPI

from .settings import get_settings
from .src.routers import auth, chat


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncIterator[None]:
    get_settings().apply_openai_env()
    yield


def create_app() -> FastAPI:
    app = FastAPI(
        title="Meridian Customer Support API",
        version="0.1.0",
        description="Stateless prototype: auth verify + streaming chat (DESIGN.md).",
        lifespan=lifespan,
    )
    app.include_router(auth.router)
    app.include_router(chat.router)

    @app.get("/health")
    async def health() -> dict[str, str]:
        return {"status": "ok"}

    return app


app = create_app()
