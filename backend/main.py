from fastapi import FastAPI

from .src.routers import auth, chat


def create_app() -> FastAPI:
    app = FastAPI(
        title="Meridian Customer Support API",
        version="0.1.0",
        description="Stateless prototype: auth verify + streaming chat (DESIGN.md).",
    )
    app.include_router(auth.router)
    app.include_router(chat.router)

    @app.get("/health")
    async def health() -> dict[str, str]:
        return {"status": "ok"}

    return app


app = create_app()
